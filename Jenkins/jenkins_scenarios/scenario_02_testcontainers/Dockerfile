FROM python:3.12-slim

# Install required system tools
RUN apt-get update \
    && apt-get install -y \
        git \
        docker.io \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Optional debug info to verify tools installed
RUN python3 --version \
    && pip --version \
    && git --version \
    && docker --version

# Set working directory
WORKDIR /workspace

# Copy scenario files
COPY requirements.txt .
COPY tests/ tests/
