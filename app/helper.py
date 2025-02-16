from io import BytesIO

import numpy as np
from PIL import Image
from fastapi import UploadFile
import os
from logger import  logger
def read_image_as_numpy(image: UploadFile) -> np.ndarray:
    """
    Reads an image file and converts it to a NumPy array.

    Args:
        image (UploadFile): The image to read.

    Returns:
        np.ndarray: The image as a NumPy array.
    """
    contents = image.file.read()  # Read the content of the image
    image_pil = Image.open(BytesIO(contents))  # Convert to a PIL image
    return np.array(image_pil)  # Convert PIL image to NumPy array


def get_file_extension(filename, default_ext):
    """Extracts the file extension, defaults if missing."""
    return os.path.splitext(filename)[-1] or default_ext


async def save_uploaded_file(upload_file, save_path):
    """Saves an uploaded file asynchronously."""
    with open(save_path, "wb") as file:
        file_data = await upload_file.read()
        file.write(file_data)
    logger.info(f"File saved: {save_path} ({len(file_data)} bytes)")
    return save_path


def delete_files(file_paths):
    """Deletes multiple files."""
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")