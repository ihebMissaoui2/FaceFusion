# Use an official PyTorch image with CUDA, cuDNN, and Python 3.11
FROM nvidia/cuda:12.4.0-base-ubuntu20.04

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for Python and other essential tools
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    curl \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    liblzma-dev \
    libffi-dev \
    libgdbm-dev \
    libnss3-dev \
    libsqlite3-dev \
    libreadline6-dev \
    libncursesw5-dev \
    git \
    libssl-dev \
    libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.7.12
RUN wget https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz && \
    tar -xvzf Python-3.7.12.tgz && \
    cd Python-3.7.12 && \
    ./configure --enable-optimizations && \
    make -j"$(nproc)" && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.7.12.tgz Python-3.7.12

# Set Python 3.7 as default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.7 1
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7 1
# Ensure pip is installed
RUN curl -sS https://bootstrap.pypa.io/pip/3.7/get-pip.py | python3.7

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
#WORKDIR /app/Wav2Lip
#RUN pip install --no-cache-dir -r requirements.txt
# Switch back to /app directory
#WORKDIR /app



# Install gdown
RUN pip install --no-cache-dir gdown

# Switch back to /app directory
#WORKDIR /app

# Download the .pth file from Google Drive
RUN gdown --id 13G3Y-OgcvBswd9t1fy8JSt1R4HlkoN-h -O /app/models/wav2lip.pth
# Install numpy before installing from requirements.txt
RUN pip install numpy
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "6000"]