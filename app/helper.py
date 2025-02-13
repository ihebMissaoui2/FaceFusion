from io import BytesIO

import numpy as np
from PIL import Image
from fastapi import UploadFile


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
