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


## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.9+ (3.11.11 is used in the Docker image)
- pip (for installing dependencies)
- Docker (if running in a container)


### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ihebMissaoui2/FaceFusion.git
cd facefusion

```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Clone Wav2Lip Model for Lip Synchronization
```bash
cd app/
git clone https://github.com/zabique/Wav2Lip
```

### 4️⃣ Download Wav2Lip Model Checkpoints
For better results, I used a pre-trained checkpoint available on Hugging Face. It is stored in my Google Drive. Run this command to download the checkpoint inside the Wav2Lip folder:

```bash
gdown --id 13G3Y-OgcvBswd9t1fy8JSt1R4HlkoN-h -O /app/Wav2Lip/wav2lip.pth
```

### 5️⃣ Install FaceSwap Model Checkpoints
Similarly, download the FaceSwap model checkpoint:

```bash
cd /app/
mkdir models
cd models
wget -P /app/models https://huggingface.co/Devia/G/resolve/main/inswapper_128.onnx
```
###  6️⃣  Run the API Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

### 7️⃣  Running with Docker
For easy usage run it with docker:

Build the Docker Image
```bash
docker build -t facefusion-api .
```
Run the Container (Limited performance of inference due to usage of  CPU for now )
```bash
docker run -p 8000:8000 facefusion-api
```
You can also specify memory and number of CPU  for example :

Note that the container requires a minimum of approximately 12GB of RAM to load the model and process video and audio.

If you have Docker Desktop installed on your personal PC, Docker by default allocates 50% of your system's memory to containers. In my case, I had to increase the memory allocation to at least 12GB to avoid issues when running inference in the Wav2Lip API.

To do this, you need to configure the .wslconfig file to prevent memory-related issues.
```bash
docker run -p 8000:8000 --cpus=32 --memory=14g facefusion-api

```

## API Endpoints
### 8️⃣  FaceSwap (POST/faceswap)
Description:Swaps a face from the source image onto the target image.

Request:

```bash
curl -X 'POST' 'http://localhost:8000/faceswap' \
-F 'target_image=@target.jpg' \
-F 'source_image=@source.jpg'
```
Response:Returns a processed image with the swapped face.

### 9️⃣   LipSync (POST /lipsync)
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

Wav2Lip primarily supports video and audio synchronization for up to 60 seconds per inference due to memory constraints and processing limitations. 

=>Workaround for Longer Videos:

  *  Segment the video into 60s chunks and process each separately.
  * Reassemble the processed clips after inference.

=>Add support of GPU acceleration for faster processing.

=>Support additional face processing features (e.g., face reenactment).


IHEB MISSAOUI (@iheb_missaoui) Feel free to contribute by submitting issues and pull requests!

License


