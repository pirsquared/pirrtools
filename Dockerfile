# Use Python 3.11 slim image for better performance
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /workspace

# Install system dependencies including Node.js and additional dev tools
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
    jq \
    tree \
    htop \
    less \
    nano \
    ssh \
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
    pip install -e .[dev] && \
    # Verify all dev tools are installed
    python -c "import pytest, black, isort, flake8, mypy, bandit, tox, sphinx; print('All dev tools verified!')"

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
    httpie

# Set up pre-commit hooks (this will be run when the container starts with a mounted volume)
RUN echo '#!/bin/bash\nif [ -f .pre-commit-config.yaml ]; then pre-commit install; fi' > /home/developer/.setup-hooks.sh && \
    chmod +x /home/developer/.setup-hooks.sh

# Create a comprehensive development setup script
RUN echo '#!/bin/bash\n\
echo "🚀 Setting up pirrtools development environment..."\n\
\n\
# Install pre-commit hooks if config exists\n\
if [ -f .pre-commit-config.yaml ]; then\n\
    echo "📋 Installing pre-commit hooks..."\n\
    pre-commit install --install-hooks\n\
    echo "✅ Pre-commit hooks installed"\n\
fi\n\
\n\
# Verify all dev tools are available\n\
echo "🔧 Verifying development tools..."\n\
python -c "import pytest, black, isort, flake8, mypy, bandit, tox, sphinx; print(\"✅ All dev tools available!\")" || echo "❌ Some dev tools missing"\n\
\n\
# Show available commands\n\
echo "\n📚 Available development commands:"\n\
echo "  pytest                    - Run tests"\n\
echo "  pytest --cov=pirrtools    - Run tests with coverage"\n\
echo "  black pirrtools/ tests/   - Format code"\n\
echo "  isort pirrtools/ tests/   - Sort imports"\n\
echo "  flake8 pirrtools/ tests/  - Check style"\n\
echo "  mypy pirrtools/           - Type checking"\n\
echo "  bandit -r pirrtools/      - Security scan"\n\
echo "  pre-commit run --all-files - Run all quality checks"\n\
echo "  tox                       - Test across Python versions"\n\
echo "  python -m build           - Build package"\n\
echo "\n🎯 Ready for development!"\n\
' > /home/developer/.setup-dev.sh && \
    chmod +x /home/developer/.setup-dev.sh

# Default command opens a bash shell
CMD ["/bin/bash"]