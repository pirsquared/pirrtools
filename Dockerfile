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
    sudo \
    ripgrep \
    fd-find \
    bat \
    exa \
    zsh \
    fish \
    tmux \
    screen \
    netcat-openbsd \
    telnet \
    iproute2 \
    pandoc \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for development with sudo privileges
RUN useradd -m -s /bin/bash developer && \
    echo 'developer ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    usermod -aG sudo developer && \
    mkdir -p /home/developer/.cache/matplotlib && \
    mkdir -p /home/developer/.local/bin && \
    mkdir -p /home/developer/.local/share && \
    chown -R developer:developer /home/developer

# Copy project files
COPY . .

# Install the package and dependencies as root first
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[dev] && \
    # Install additional development tools for performance and modern workflow
    pip install --upgrade \
        ruff \
        bandit \
        nox \
        hatch \
        rich-cli && \
    # Verify all modern dev tools are installed
    python -c "import pytest, black, isort, mypy, tox, sphinx, ruff, bandit, nox; print('✅ All modern dev tools verified!')"

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
    nbsphinx \
    ipykernel \
    rich \
    httpie

# Create a convenience script for serving docs
RUN echo '#!/bin/bash\n\
if [ -d "docs/_build/html" ]; then\n\
    echo "📖 Serving docs from docs/_build/html on port 8080..."\n\
    cd docs/_build/html && python -m http.server 8080 --bind 0.0.0.0\n\
elif [ -d "docs" ]; then\n\
    echo "📖 Building docs first..."\n\
    cd docs && make html\n\
    echo "📖 Serving docs from docs/_build/html on port 8080..."\n\
    cd _build/html && python -m http.server 8080 --bind 0.0.0.0\n\
else\n\
    echo "❌ No docs directory found"\n\
    exit 1\n\
fi\n\
' > /home/developer/.local/bin/serve-docs && \
    chmod +x /home/developer/.local/bin/serve-docs

# Create a convenience script for starting Jupyter Lab
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Jupyter Lab on port 8888..."\n\
echo "📁 Working directory: /workspace"\n\
echo "🔗 Access at: http://localhost:8888"\n\
echo ""\n\
# Create notebooks directory if it doesnt exist\n\
mkdir -p /workspace/notebooks\n\
# Start Jupyter Lab with configuration for container use\n\
jupyter lab \\\n\
    --ip=0.0.0.0 \\\n\
    --port=8888 \\\n\
    --no-browser \\\n\
    --allow-root \\\n\
    --NotebookApp.token=\"\" \\\n\
    --NotebookApp.password=\"\" \\\n\
    --NotebookApp.allow_origin=\"*\" \\\n\
    --NotebookApp.disable_check_xsrf=True \\\n\
    --notebook-dir=/workspace\n\
' > /home/developer/.local/bin/start-jupyter && \
    chmod +x /home/developer/.local/bin/start-jupyter

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
python -c "import pytest, black, isort, mypy, tox, sphinx, ruff, bandit, nox; print(\"✅ All modern dev tools available!\")" || echo "❌ Some dev tools missing"\n\
\n\
# Show version information for key tools\n\
echo "📋 Tool versions:"\n\
python --version\n\
black --version 2>/dev/null | head -1 || echo "  black: not available"\n\
ruff --version 2>/dev/null || echo "  ruff: not available"\n\
mypy --version 2>/dev/null || echo "  mypy: not available"\n\
pytest --version 2>/dev/null | head -1 || echo "  pytest: not available"\n\
\n\
# Start Sphinx docs server in background if docs exist\n\
if [ -d "docs/_build/html" ]; then\n\
    echo "📖 Starting Sphinx docs server on port 8080..."\n\
    cd docs/_build/html && python -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &\n\
    echo "✅ Docs server started at http://localhost:8080"\n\
    cd /workspace\n\
elif [ -d "docs" ]; then\n\
    echo "📖 Building and serving Sphinx docs..."\n\
    cd docs && make html > /dev/null 2>&1 && cd _build/html && python -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &\n\
    echo "✅ Docs built and server started at http://localhost:8080"\n\
    cd /workspace\n\
fi\n\
\n\
# Show available commands\n\
echo "\n📚 Available development commands:"\n\
echo "  🧪 Testing & Quality:"\n\
echo "    pytest                    - Run tests"\n\
echo "    pytest --cov=pirrtools    - Run tests with coverage"\n\
echo "    tox                       - Test across Python versions"\n\
echo "    nox                       - Modern testing with Python config"\n\
echo ""\n\
echo "  🎨 Code Formatting & Linting:"\n\
echo "    black pirrtools/ tests/   - Format code (official formatter)"\n\
echo "    ruff check pirrtools/     - Fast linting (replaces flake8/pylint)"\n\
echo "    ruff format pirrtools/    - Fast formatting (alternative to black)"\n\
echo "    isort pirrtools/ tests/   - Sort imports"\n\
echo "    mypy pirrtools/           - Type checking"\n\
echo ""\n\
echo "  🔒 Security & Analysis:"\n\
echo "    bandit -r pirrtools/      - Security vulnerability scanning"\n\
echo "    pre-commit run --all-files - Run all quality checks"\n\
echo ""\n\
echo "  📦 Building & Publishing:"\n\
echo "    python -m build           - Build package (traditional)"\n\
echo "    hatch build               - Build package (modern)"\n\
echo "    twine upload dist/*       - Upload to PyPI"\n\
echo "\n📖 Documentation:"\n\
echo "  make -C docs html         - Build Sphinx docs (includes notebooks)"\n\
echo "  serve-docs                - Start docs server on port 8080"\n\
echo "\n🎮 Interactive Development:"\n\
echo "  start-jupyter             - Start Jupyter Lab on port 8888"\n\
echo "  ipython                   - Start IPython REPL"\n\
echo "\n🎯 Ready for development!"\n\
' > /home/developer/.setup-dev.sh && \
    chmod +x /home/developer/.setup-dev.sh

# Default command opens a bash shell
CMD ["/bin/bash"]