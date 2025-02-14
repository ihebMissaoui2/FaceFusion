FROM python:3.9-slim

WORKDIR /app

RUN mkdir /app/models

RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

#faceswap model downloading
RUN wget -P /app/models https://huggingface.co/Devia/G/resolve/main/inswapper_128.onnx

RUN apt-get update && apt-get install -y git
#lipsync model downloading and dependencies installation
# Clone the Wav2Lipp repository
RUN git clone https://github.com/zabique/Wav2Lip

# Change to Wav2Lipp directory and install dependencies
WORKDIR /app/Wav2Lip
RUN pip install --no-cache-dir -r requirements.txt
# Switch back to /app directory
WORKDIR /app



# Install gdown
RUN pip install --no-cache-dir gdown

# Switch back to /app directory
WORKDIR /app

# Download the .pth file from Google Drive
RUN gdown --id 13G3Y-OgcvBswd9t1fy8JSt1R4HlkoN-h -O /app/models/wav2lip.pth

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install librosa==0.8.0
COPY app /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "600"]
