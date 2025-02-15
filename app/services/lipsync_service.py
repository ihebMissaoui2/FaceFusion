import os
import shutil
import tempfile
import subprocess
from fastapi.responses import FileResponse
from logger import logger

UPLOAD_DIR = "/app/Wav2Lip"  # Permanent storage directory

def process_lipsync(video, audio):
    """
    Processes the LipSync operation synchronously using subprocess.run.

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

        # Construct the inference command
        # Change to the Wav2Lip subfolder
        os.chdir("/app/Wav2Lip")
        logger.info(f"{os.getcwd()}  # Get current working directory")

        # Define paths using os.path.join() to ensure cross-platform compatibility
        inference_command = [
            "python", "inference.py",
            "--checkpoint_path", "wav2lip.pth",
            "--face",  audio_new_path,
            "--audio", video_new_path,
        ]
        logger.info(f"{os.getcwd()}  # Get current working directory")
        # Change to the Wav2Lip subfolder
        os.chdir("/app/Wav2Lip")
        logger.info(f"Running inference command: {' '.join(inference_command)}")

        # Run the command and capture output in real-time
        process = subprocess.Popen(
            inference_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Stream logs in real-time
        def stream_output(stream, log_func):
            for line in iter(stream.readline, ''):
                log_func(line.strip())
            stream.close()

        # Stream both stdout and stderr
        stream_output(process.stdout, logger.info)
        stream_output(process.stderr, logger.error)

        # Wait for process completion
        return_code = process.wait()

        if return_code != 0:
            raise RuntimeError(f"Inference failed with return code {return_code}")

        logger.info("Inference completed successfully.")

        # Assuming the result produces an output video file
        output_video_path = "/app/Wav2Lip/results/result_voice.mp4"  # Modify if needed

        if not os.path.exists(output_video_path):
            raise FileNotFoundError("Output video file was not created.")

        logger.info("Returning the processed video as a file response.")
        return FileResponse(output_video_path, media_type="video/mp4", filename="output_video.mp4")

    except Exception as e:
        logger.error(f"An error occurred while running the inference command: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
