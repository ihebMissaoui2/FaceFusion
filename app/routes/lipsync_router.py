from fastapi import APIRouter, UploadFile, File

from services.lipsync_service import process_lipsync

router = APIRouter()


@router.post("/lipsync")
async def lipsync(video: UploadFile = File(...), audio: UploadFile = File(...)):
    """
    Synchronize lip movements in a video with an audio file.

    Args:
        video (UploadFile): The input video file.
        audio (UploadFile): The input audio file to be synced.

    Returns:
        FileResponse: The processed video with synchronized audio.
    """
    return await process_lipsync(video, audio)
