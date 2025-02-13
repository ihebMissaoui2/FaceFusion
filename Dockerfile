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

RUN wget -P /app/models https://huggingface.co/Devia/G/resolve/main/inswapper_128.onnx
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
