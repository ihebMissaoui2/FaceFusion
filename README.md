# FaceFusion API

## Overview
FaceFusion API is a containerized FastAPI-based application that provides endpoints for:

- **FaceSwap**: Swap faces between two images.
- **LipSync**: Sync an audio file with a video.

The API is packaged inside a Docker container for easy deployment and scalability.

## Features
- FastAPI framework for high performance.
- Dockerized for easy deployment.
- Multithreaded execution (supports multiple workers for better performance).
- Swagger UI documentation available at `/docs`.
- Minimal processing delay:
  - FaceSwap: ≤ 5s
  - LipSync: ≤ 10s

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- Docker (if running in a container)
- pip (for installing dependencies)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/facefusion-api.git
cd facefusion-api
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the API Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

### 4️⃣ Running with Docker
Build the Docker Image
```bash
docker build -t facefusion-api .
```
Run the Container
```bash
docker run -p 8000:8000 facefusion-api
```

## API Endpoints
### 1️⃣ FaceSwap (POST /faceswap)
Description:Swaps a face from the source image onto the target image.

Request:

```bash
curl -X 'POST' 'http://localhost:8000/faceswap' \
-F 'target_image=@target.jpg' \
-F 'source_image=@source.jpg'
```
Response:Returns a processed image with the swapped face.

### 2️⃣ LipSync (POST /lipsync)
Description: Synchronizes an audio file with a video.

Request:
```bash
curl -X 'POST' 'http://localhost:8000/lipsync' \
-F 'video=@input.mp4' \
-F 'audio=@input.wav'
```
Response:
Returns a video file with synchronized lip movements.


# Future Enhancements
Add GPU acceleration for faster processing.

Support additional face processing features (e.g., face reenactment).
Contributors

IHEB MISSAOUI (@iheb_missaoui) Feel free to contribute by submitting issues and pull requests!

License
This project have no licence.


