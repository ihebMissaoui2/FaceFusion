import os
import subprocess
import threading

from fastapi.responses import FileResponse

from helper import get_file_extension, save_uploaded_file, delete_files
from logger import logger

UPLOAD_DIR = "Wav2Lip"  # Temporary storage directory for inference


def run_inference_command(video_filename, audio_filename):
    try:
        """Runs the Wav2Lip inference command and logs output in real-time."""
        inference_command = [
            "python", "inference.py",
            "--checkpoint_path", "wav2lip.pth",
            "--face", video_filename,
            "--audio", audio_filename,
        ]
        logger.info(f"Running inference command: {' '.join(inference_command)}")

        def stream_output(stream, log_func):
            """Streams subprocess output in real-time."""
            try:
                for line in iter(stream.readline, ''):
                    log_func(line.strip())
            finally:
                stream.close()

        # Run subprocess
        process = subprocess.Popen(
            inference_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, logger.info))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, logger.warning))
        stdout_thread.start()
        stderr_thread.start()

        return_code = process.wait(timeout=2000)  # Wait for completion
        stdout_thread.join()
        stderr_thread.join()

        if return_code != 0:
            raise RuntimeError(f"Inference failed with return code {return_code}")

        logger.info("Inference completed successfully.")
    except subprocess.TimeoutExpired:
        logger.error("Inference process timed out after 20 minutes.")
        process.kill()
        return {"status": "error", "message": "Inference process took too long and was terminated."}


async def process_lipsync(video, audio):
    """Processes the LipSync operation and returns the output video."""
    logger.info(f"Received video: {video.filename}, audio: {audio.filename}")

    try:
        # Change working directory to Wav2Lip
        os.chdir(UPLOAD_DIR)
        # Extract file extensions
        video_ext = get_file_extension(video.filename, ".mp4")
        audio_ext = get_file_extension(audio.filename, ".wav")
        #  file names
        video_name = f"video{video_ext}"
        audio_name= f"audio{audio_ext}"

        # Save files
        await save_uploaded_file(video, video_name)
        await save_uploaded_file(audio, audio_name)

        # Run inference
        run_inference_command(video_name, audio_name)
        # back to root
        os.chdir("..")
        # Output file path
        output_video_path = os.path.join(UPLOAD_DIR,"results", "result_voice.mp4")
        if not os.path.exists(output_video_path):
            raise FileNotFoundError("Output video file was not created.")

        # Cleanup temporary inputs files

        delete_files([video_name,audio_name])


        # Add the cleanup task which will be triggered after sending the file(because the user wait for the file for now ).

        logger.info("Returning the processed video as a file response.")

        return FileResponse(output_video_path, media_type="video/mp4", filename="lipsync_generated_video.mp4")



    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        delete_files([video_name, audio_name])  # Cleanup on failure
        return {"status": "error", "message": str(e)}

    #finally:
     #   os.chdir("..")  # Restore original directory
