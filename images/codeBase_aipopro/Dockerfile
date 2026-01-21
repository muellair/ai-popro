FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Base tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /codeBase

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade pip \
 && python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/evaluate.py .
COPY src/train_nn.py .
COPY README.md .

# silence noisy tensorflow logging
ENV TF_CPP_MIN_LOG_LEVEL=3

# Default shell
CMD ["bash"]
