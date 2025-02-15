import tempfile

from fastapi.responses import FileResponse
import subprocess
from logger import logger
import shutil

import os
async def process_lipsync(video, audio):
    """
    Processes the LipSync operation.

    Reads the uploaded video and audio files, synchronizes them using ,
    and returns the processed video.

    Args:
        video (UploadFile): The input video file.
        audio (UploadFile): The input audio file.

    Returns:
        : The synchronized video file.
    """
        #logger.info(f"Received video: {video.filename}, audio: {audio.filename}")

    try:
        # Save video file temporarily
    #    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
     #       video_data = await video.read()
      #      temp_video.write(video_data)
       #     video_path = temp_video.name
        #    logger.info(f"Temporary video file saved at: {video_path} ({len(video_data)} bytes)")
        #UPLOAD_DIR = "/app/models"  # Permanent storage directory
        # Move video file to permanent location
        #video_new_path = os.path.join(UPLOAD_DIR, video.filename)
        #shutil.move(video_path, video_new_path)

        # Save audio file temporarily
        #with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        #    audio_data = await audio.read()
         #   temp_audio.write(audio_data)
          #  audio_path = temp_audio.name
           # logger.info(f"Temporary audio file saved at: {audio_path} ({len(audio_data)} bytes)")
        # Move audio file to permanent location
        #audio_new_path = os.path.join(UPLOAD_DIR, audio.filename)
        #shutil.move(audio_path, audio_new_path)
        # Construct the inference command with the dynamic paths
        temp_dir = '/app/Wav2Lip/temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        inference_command = [
            "python3", "Wav2Lip/inference.py",
            "--checkpoint_path", "models/wav2lip.pth",
            "--face", "models/Kevin Surace_talk.mp4",
            "--audio", "models/final_obbama_54_second.wav"
        ]



        logger.info(f"Running inference command: {' '.join(inference_command)}")

        # Use Popen to run the command and stream the output
        process = subprocess.Popen(
            inference_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Stream the output in real-time
        for line in process.stdout:
            logger.info(line.strip())  # Log the standard output

        # Capture stderr (error output)
        for line in process.stderr:
            logger.error(line.strip())  # Log the error output

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        if return_code == 0:
            logger.info("Inference completed successfully.")
        else:
            logger.error(f"Inference failed with return code {return_code}")

        # Assuming the result produces an output video file, replace this path with the actual path
        output_video_path = "Wav2Lip/results/result_voice.mp4"  # Modify with actual path if needed

        logger.info("Returning the processed video as a file response.")
        # Returning the video as a file response
        return FileResponse(output_video_path, media_type="video/mp4", filename="output_video.mp4")

    except subprocess.TimeoutExpired as e:
            logger.error(f"Inference command timed out: {e}")
            return {"status": "error", "message": "Inference command timed out"}
    except Exception as e:
            logger.error(f"An error occurred while running the inference command: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
