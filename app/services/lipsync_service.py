import os
import shutil
import tempfile
import subprocess
import threading
from fastapi.responses import FileResponse
from logger import logger

UPLOAD_DIR = "Wav2Lip"  # Permanent storage directory


async def process_lipsync(video, audio):
    """
    Processes the LipSync operation synchronously using subprocess with real-time logging.

    Args:
        video (UploadFile): The input video file.
        audio (UploadFile): The input audio file.

    Returns:
        FileResponse: The synchronized video file.
    """
    logger.info(f"Received video: {video.filename}, audio: {audio.filename}")

    try:
        # Save video file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            video_data = video.file.read()
            temp_video.write(video_data)
            video_path = temp_video.name

        logger.info(f"Temporary video file saved at: {video_path} ({len(video_data)} bytes)")

        # Move video file to permanent location
        video_new_path = os.path.join(UPLOAD_DIR, video.filename)
        shutil.move(video_path, video_new_path)

        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_data = audio.file.read()
            temp_audio.write(audio_data)
            audio_path = temp_audio.name

        logger.info(f"Temporary audio file saved at: {audio_path} ({len(audio_data)} bytes)")

        # Move audio file to permanent location
        audio_new_path = os.path.join(UPLOAD_DIR, audio.filename)
        shutil.move(audio_path, audio_new_path)

        # Change to the Wav2Lip subfolder
        os.chdir("Wav2Lip")
        logger.info(f"Current working directory: {os.getcwd()}")

        # Define the inference command
        inference_command = [
            "python", "inference.py",
            "--checkpoint_path", "wav2lip.pth",
            "--face", video.filename,
            "--audio", audio.filename,
        ]

        logger.info(f"Running inference command: {' '.join(inference_command)}")

        # Function to stream real-time logs
        def stream_output(stream, log_func):
            try:
                for line in iter(stream.readline, ''):
                    log_func(line.strip())
            finally:
                stream.close()

        # Run inference command with Popen
        process = subprocess.Popen(
            inference_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Start threads to capture stdout and stderr
        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, logger.info))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, logger.error))
        stdout_thread.start()
        stderr_thread.start()

        # Wait up to 10 minutes for process to complete
        return_code = process.wait(timeout=2000)
        stdout_thread.join()
        stderr_thread.join()

        if return_code != 0:
            raise RuntimeError(f"Inference failed with return code {return_code}")

        logger.info("Inference completed successfully.")

        # Path to the generated video output
        output_video_path = "results/result_voice.mp4"
        if not os.path.exists(output_video_path):
            raise FileNotFoundError("Output video file was not created.")

        logger.info("Returning the processed video as a file response.")
        return FileResponse(output_video_path, media_type="video/mp4", filename="output_video.mp4")

    except subprocess.TimeoutExpired:
        logger.error("Inference process timed out after 10 minutes.")
        process.kill()
        return {"status": "error", "message": "Inference process took too long and was terminated."}

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
