FROM ubuntu:22.04

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

# Create non-root user (important for VS Code + Docker)
RUN useradd -ms /bin/bash dev

# Make workspace and copy requirements into the image (so pip can see it)
WORKDIR /workspace
COPY --chown=dev:dev requirements.txt /workspace/

USER dev

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Python tooling
ENV PATH="/home/dev/.local/bin:$PATH"