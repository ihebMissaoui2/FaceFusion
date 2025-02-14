import io
import cv2
import insightface
import numpy as np


from logger import logger  # Import the logger

async def process_faceswap(target_image: np.ndarray, source_image: np.ndarray):
    """
    Process a face swap between two images.

    Args:
        target_image (np.ndarray): The target image where the face will be swapped.
        source_image (np.ndarray): The source image containing the face to be swapped.

    Returns:
        io.BytesIO: The processed image as a byte stream.
    """
    logger.info("Starting face swap process.")

    try:
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]

        # Initialize face analyser
        logger.info("Initializing face analysis model.")
        FACE_ANALYSER = insightface.app.FaceAnalysis(
            name="buffalo_l",
            root=".",
            providers=providers,
            allowed_modules=["landmark_3d_68", "landmark_2d_106", "detection", "recognition"]
        )
        FACE_ANALYSER.prepare(ctx_id=0, det_size=(640, 640))
        logger.info("Face analysis model initialized successfully.")

        # Identify faces in source image
        src_faces = FACE_ANALYSER.get(source_image)
        if not src_faces:
            logger.error("No faces detected in source image.")
            return {"error": "No faces detected in source image."}

        # Identify faces in target image
        target_faces = FACE_ANALYSER.get(target_image)
        if not target_faces:
            logger.error("No faces detected in target image.")
            return {"error": "No faces detected in target image."}

        # Load face swap model
        model_path = 'models/inswapper_128.onnx'
        logger.info(f"Loading face swap model from {model_path}.")
        model_swap_insightface = insightface.model_zoo.get_model(model_path, providers=providers)
        logger.info("Face swap model loaded successfully.")

        # Perform face swap
        logger.info("Performing face swap.")
        img_fake = model_swap_insightface.get(
            img=target_image,
            target_face=target_faces[0],
            source_face=src_faces[0],
            paste_back=True
        )
        logger.info("Face swap completed successfully.")

        # Convert the image to RGB
        img_fake_rgb = cv2.cvtColor(img_fake, cv2.COLOR_BGR2RGB)

        # Encode the image as JPEG
        is_success, buffer = cv2.imencode(".jpg", img_fake_rgb)
        if not is_success:
            logger.error("Failed to encode face-swapped image.")
            return {"error": "Failed to generate image."}

        # Convert to byte stream
        byte_io = io.BytesIO(buffer)
        logger.info("Face-swapped image successfully generated and converted to byte stream.")

        return byte_io

    except Exception as e:
        logger.error(f"Error during face swap processing: {e}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}
