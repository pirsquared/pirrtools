# Use Python 3.11 slim image for better performance
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /workspace

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    vim \
    wget \
    unzip \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for development
RUN useradd -m -s /bin/bash developer && \
    mkdir -p /home/developer/.cache/matplotlib && \
    mkdir -p /home/developer/.local/bin && \
    mkdir -p /home/developer/.local/share && \
    chown -R developer:developer /home/developer

# Copy project files
COPY . .

# Install the package and dependencies as root first
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[dev]

# Switch to developer user
USER developer

# Set up PATH for user-installed tools
ENV PATH="/home/developer/.local/bin:$PATH" \
    MPLCONFIGDIR="/home/developer/.cache/matplotlib"

# Install Claude Code CLI and other tools in user space
RUN npm config set prefix '/home/developer/.local' && \
    npm install -g @anthropic-ai/claude-code

# Install additional useful development tools in user space
RUN pip install --user \
    ipython \
    jupyter \
    jupyterlab \
    rich \
    httpie \
    pre-commit

# Default command opens a bash shell
CMD ["/bin/bash"]