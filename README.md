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



## Project Structure

```plaintext
app/
├── routes/                 # API route handlers
│   ├── faceswap_router.py  # FaceSwap endpoint
│   ├── lipsync_router.py   # LipSync endpoint
│   └── __init__.py
│
├── services/               # Core processing logic
│   ├── faceswap_service.py # FaceSwap processing (InsightFace)
│   ├── lipsync_service.py  # LipSync processing (Wav2Lip)
│   └── __init__.py
│
├── main.py                 # FastAPI initialization and route registration
├── logger.py               # Logging configuration
├── helper.py               # Utility functions for image/video processing
│
├── Dockerfile              # Containerization setup
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

app/routes/

Contains route handlers for API endpoints.

- faceswap_router.py: Defines an endpoint that takes two images as input, calls the FaceSwap service, and returns the generated image.
- lipsync_router.py: Defines an endpoint that takes a video and an audio file, calls the LipSync service, and returns the synchronized video.

app/services/

Contains the core processing logic and model inference.

- faceswap_service.py: Uses insightface and inswapper_128 to swap faces between images.
- lipsync_service.py: Uses Wav2Lip to synchronize lip movements with the provided audio.

app/ (root folder)

- main.py: Initializes FastAPI and registers the routes .
- logger.py: Configures logging for the application.
- helper.py: Contains generic utility functions for processing images and videos.

Other files

- Dockerfile: Defines the environment for running the API in a container.
- requirements.txt: Lists required dependencies.
- README.md: Provides project documentation.


## Installation  (With docker)

###   Running with Docker using CPU
For easy usage run it with docker:

Build the Docker Image
```bash
docker build -t facefusion-api .
```
Run the Container (using CPU for  )
```bash
docker run --name facefusion-container -p 8000:8000 facefusion-api
```
You can also specify memory and number of CPU  for example :

Note that the container requires a minimum of approximately 12GB of RAM to load the model and process video and audio.

If you have Docker Desktop installed on your personal PC, Docker by default allocates 50% of your system's memory to containers. In my case, I had to increase the memory allocation to at least 12GB to avoid issues when running inference in the Wav2Lip API.
To do this, you need to configure the .wslconfig file to prevent memory-related issues.
###   Running with Docker using GPU

To run the models using GPU for better inference time use : 
```bash
docker run -d -p 8000:8000  --name lypsyncontainer --runtime=nvidia --gpus all facefusion-api


```
Note that Wav2Lip model need 15gb of GPU VRAM to due inference
## Installation & Setup (Without docker)

### Prerequisites
Ensure you have the following installed:
- Python 3.9+ (3.11.11 is used in the Docker image)
- pip (for installing dependencies)
- Docker (if running in a container)
- Build a new virtual environment for this API.

### 1️⃣ Download the folder of this Api and change directory to the root of the Repository
```bash
cd facefusionapi

```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Download Wav2Lip(open source model) for Lip Synchronization
```bash
cd app
Download and extract the open source Wav2Lip model folder with Wav2Lip name from  https://github.com/zabique/Wav2Lip
or 
git clone https://github.com/zabique/Wav2Lip
```

### 4️⃣ Download Wav2Lip Model Checkpoints
For better results, I used a pre-trained checkpoint available on Hugging Face.  Run this command to download the checkpoint inside the Wav2Lip folder:

```bash
gdown --id 13G3Y-OgcvBswd9t1fy8JSt1R4HlkoN-h -O Wav2Lip/wav2lip.pth
```

### 5️⃣ Install FaceSwap Model Checkpoints
Similarly, download the FaceSwap model checkpoint:

```bash
mkdir models
cd models
wget -P models https://huggingface.co/Devia/G/resolve/main/inswapper_128.onnx
```
###  6️⃣  Run the API Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```


## API Endpoints
### 1️⃣  FaceSwap (POST/faceswap)
Description:Swaps a face from the source image onto the target image.

Request:

```bash
curl -X 'POST' 'http://localhost:8000/faceswap' \
-F 'target_image=@target.jpg' \
-F 'source_image=@source.jpg'
```
Response:Returns a processed image with the swapped face.

### 2️⃣   LipSync (POST /lipsync)
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

Wav2Lip primarily supports video and audio synchronization for up to 60 seconds per inference . 

=>Workaround for Longer Videos:

  *  Segment the video into 60s chunks and process each separately.
  * Reassemble the processed clips after inference.







