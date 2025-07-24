# Use Python 3.11 slim image for better performance
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first for better Docker layer caching
COPY pyproject.toml .

# Install dependencies (including dev dependencies)
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[dev]

# Copy the rest of the project
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Create a non-root user for development
RUN useradd -m -s /bin/bash developer && \
    chown -R developer:developer /workspace
USER developer

# Default command opens a bash shell
CMD ["/bin/bash"]