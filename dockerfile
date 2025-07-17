# Use a full-featured Python base image that supports compilation
FROM python:3.11-slim

# Set environment variables to avoid prompts and enable UTF-8
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Install system packages needed to build numpy and scikit-learn
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source files
COPY requirements.txt ./
COPY app.py dto.py mappers.py matching.py ./

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Define entry point for Lambda compatibility (optional)
CMD ["app.lambda_handler"]
