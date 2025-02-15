FROM python:3.11-slim

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




# Install gdown
RUN pip install --no-cache-dir gdown


# Download the .pth file from Google Drive
RUN gdown --id 13G3Y-OgcvBswd9t1fy8JSt1R4HlkoN-h -O /app/Wav2Lip/wav2lip.pth

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install ffmpeg dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*
RUN pip install audioread==3.0.1 certifi==2025.1.31 cffi==1.17.1 charset-normalizer==3.4.1 colorama==0.4.6 decorator==5.1.1 filelock==3.17.0 fsspec==2025.2.0 idna==3.10 Jinja2==3.1.5 joblib==1.4.2 lazy_loader==0.4 librosa==0.9.1 llvmlite==0.44.0 MarkupSafe==3.0.2 mpmath==1.3.0 msgpack==1.1.0 networkx==3.4.2 numba==0.61.0 numpy==2.1.3 opencv-contrib-python==4.11.0.86 opencv-python==4.11.0.86 packaging==24.2 pillow==11.1.0 pip==25.0 platformdirs==4.3.6 pooch==1.8.2 pycparser==2.22 requests==2.32.3 resampy==0.4.3 scikit-learn==1.6.1 scipy==1.15.1 setuptools==75.8.0 soundfile==0.13.1 soxr==0.5.0.post1 sympy==1.13.1 threadpoolctl==3.5.0 torch==2.6.0 torchvision==0.21.0 tqdm==4.67.1 typing_extensions==4.12.2 urllib3==2.3.0 wheel==0.45.1

COPY app /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "10000"]
