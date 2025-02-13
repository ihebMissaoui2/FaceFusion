import ffmpeg
from io import BytesIO
from fastapi.responses import FileResponse

async def process_lipsync(video, audio):
    """
    Processes the LipSync operation.

    Reads the uploaded video and audio files, synchronizes them using FFmpeg,
    and returns the processed video.

    Args:
        video (UploadFile): The input video file.
        audio (UploadFile): The input audio file.

    Returns:
        FileResponse: The synchronized video file.
    """
    video_bytes = await video.read()
    audio_bytes = await audio.read()

    # Output file path
    output_video_path = "output_lipsync.mp4"

    # Process LipSync using FFmpeg
    input_video = BytesIO(video_bytes)
    input_audio = BytesIO(audio_bytes)

    (
        ffmpeg
        .input(input_video)
        .input(input_audio)
        .output(output_video_path, vcodec='copy', acodec='aac', strict='experimental')
        .run(overwrite_output=True)
    )

    return FileResponse(output_video_path)
