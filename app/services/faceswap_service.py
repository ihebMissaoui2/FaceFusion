import io

import cv2
import insightface
import numpy as np


async def process_faceswap(target_image: np.ndarray, source_image: np.ndarray):
    """
    Process a face swap between two images.

    Args:
        target_image (np.ndarray): The target image where the face will be swapped.
        source_image (np.ndarray): The source image containing the face to be swapped.

    Returns:

    """
    # Implement the face swap logic here
    # This could involve using a library or model to swap faces in the images

    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    # identify faces
    FACE_ANALYSER = insightface.app.FaceAnalysis(
        name="buffalo_l",
        root=".", providers=providers, allowed_modules=["landmark_3d_68", "landmark_2d_106", "detection", "recognition"]
    )
    FACE_ANALYSER.prepare(
        ctx_id=0,
        det_size=(640, 640),
    )
    src_faces = FACE_ANALYSER.get(source_image)
    model_path = 'models/inswapper_128.onnx'
    model_swap_insightface = insightface.model_zoo.get_model(model_path, providers=providers)
    img_fake = model_swap_insightface.get(img=target_image, target_face=FACE_ANALYSER.get(target_image)[0],
                                          source_face=src_faces[0], paste_back=True)
    # Convert the image to RGB (if needed)
    img_fake_rgb = cv2.cvtColor(img_fake, cv2.COLOR_BGR2RGB)

    # Convert the image to a byte stream without encoding to PNG/JPEG
    is_success, buffer = cv2.imencode(".jpg", img_fake_rgb)  # Can also use '.jpg' or '.bmp', etc.

    # If the conversion was successful, we can stream the image
    if is_success:
        # Convert the buffer to a byte stream
        byte_io = io.BytesIO(buffer)

        # Return the byte stream
        return byte_io

    # In case of failure
    return {"error": "Failed to generate image"}
