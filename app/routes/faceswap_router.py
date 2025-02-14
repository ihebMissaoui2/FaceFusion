from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from helper import read_image_as_numpy
from services.faceswap_service import process_faceswap
from logger import  logger
router = APIRouter()


@router.post("/faceswap")
async def faceswap(target_image: UploadFile = File(...), source_image: UploadFile = File(...)):
    """
    Perform a face swap between two images.

    Args:
        target_image (UploadFile): The image where the face will be swapped.
        source_image (UploadFile): The image containing the face to be swapped.

    Returns:
        FileResponse: The processed image with the swapped face.
    """
    logger.info(
        f"Faceswap API called with target_image: {target_image.filename}, source_image: {source_image.filename}")

    try:
        # Read images as NumPy arrays using the generic function
        target_array = read_image_as_numpy(target_image)
        source_array = read_image_as_numpy(source_image)
        logger.info("Successfully read both images as NumPy arrays.")

        # Pass NumPy arrays to face swap service
        img_io = await process_faceswap(target_array, source_array)
        logger.info("Face swap processing completed successfully.")

        return StreamingResponse(img_io, media_type="image/png")

    except Exception as e:
        logger.error(f"Error during face swap processing: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
