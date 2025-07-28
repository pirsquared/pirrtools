# Container Development Environment

This document describes the containerized development environment for pirrtools with all development tools pre-installed.

## 🐳 Container Features

### Development Tools Included
All development tools are pre-installed and verified in the container:

- **Testing**: pytest, pytest-cov, pytest-xdist, tox
- **Code Quality**: black, isort, flake8, mypy, pylint, bandit
- **Documentation**: sphinx, sphinx-rtd-theme, sphinx-autodoc-typehints
- **Build & Publishing**: build, twine, wheel
- **Development**: pre-commit, ipython, jupyter, jupyterlab
- **System Tools**: git, node, npm, curl, vim, nano

### Container Configuration Files
- **Dockerfile**: Multi-stage container with all dev tools
- **docker-compose.yml**: Service configuration with volume mounts
- **.devcontainer/devcontainer.json**: VS Code integration

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Build and start the container
docker-compose up -d

# Enter the container
docker-compose exec pirrtools-dev bash

# Container will automatically:
# - Install pre-commit hooks
# - Verify all dev tools
# - Show available commands
```

### Option 2: VS Code Dev Container
1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Click "Reopen in Container" when prompted
4. VS Code will build and connect to the container automatically

### Option 3: Direct Docker Build
```bash
# Build the container
docker build -t pirrtools-dev .

# Run the container
docker run -it -v $(pwd):/workspace pirrtools-dev
```

## 🛠️ Container Scripts

### Automatic Setup Script
The container runs `/home/developer/.setup-dev.sh` on startup which:
- Installs pre-commit hooks automatically
- Verifies all development tools are available
- Shows available development commands
- Provides a ready-to-use development environment

### Verification Script
Use `./scripts/verify-container.sh` to verify the container setup:
```bash
# Inside the container
./scripts/verify-container.sh
```

This checks:
- Python environment and pip
- All development tools (pytest, black, isort, etc.)
- Python package imports
- System tools availability
- Configuration files
- pirrtools installation
- Quick test run

## 📦 Pre-installed Development Environment

### Python Environment
- **Python 3.11** with pip, setuptools, wheel
- **pirrtools** installed in development mode (`pip install -e .[dev]`)
- All dev dependencies from `pyproject.toml`

### VS Code Extensions (DevContainer)
- Python core tools (python, black-formatter, pylint, isort, mypy)
- Testing tools (pytest, test adapters)
- Code quality (ruff, flake8)
- Documentation (docstring-generator, rst)
- Git integration (gitlens)
- Development utilities (todo-tree, toml support)

### Volume Mounts
- **Source code**: `/workspace` (mounted from host)
- **Cache persistence**: `/home/developer/.cache` (persistent volume)
- **Pre-commit cache**: `/home/developer/.cache/pre-commit` (persistent volume)

## 🔧 Development Workflow

### Inside the Container
```bash
# Run tests
pytest
pytest --cov=pirrtools

# Code quality checks
black pirrtools/ tests/
isort pirrtools/ tests/
flake8 pirrtools/ tests/
mypy pirrtools/
bandit -r pirrtools/

# Run all quality checks
pre-commit run --all-files

# Cross-version testing
tox

# Build package
python -m build

# Use the Makefile for common tasks
make help
make test
make lint
make format
```

### VS Code Integration
When using the Dev Container with VS Code:
- **Auto-formatting** on save (black + isort)
- **Linting** with flake8, pylint, mypy, bandit
- **Testing** integration with pytest
- **Type checking** with mypy
- **IntelliSense** with full package context
- **Integrated terminal** with all tools available

## 🚀 Available Make Commands

Use the included `Makefile` for common development tasks:

```bash
make help              # Show all available commands
make install           # Install in development mode
make install-hooks     # Install pre-commit hooks
make test              # Run tests
make test-cov         # Run tests with coverage
make lint             # Run all linting tools
make format           # Format code
make type-check       # Run mypy
make security         # Run bandit security scan
make pre-commit       # Run all pre-commit hooks
make docs             # Build documentation
make build            # Build package
make clean            # Clean build artifacts
make container        # Build container
make verify-container # Verify container setup
```

## 🔍 Container Verification

The container includes comprehensive verification to ensure all tools work correctly:

```bash
# Run verification script
./scripts/verify-container.sh

# Or use make command
make verify-container
```

### What Gets Verified
✅ Python environment and pip  
✅ All development tools (pytest, black, isort, flake8, mypy, bandit, etc.)  
✅ Python package imports  
✅ System tools (git, node, npm, curl)  
✅ Configuration files  
✅ pirrtools installation  
✅ Quick test execution  
✅ Pre-commit hooks setup  

## 🎯 Container Benefits

### Consistency
- **Same environment** across all developers
- **Version-locked** development tools
- **Pre-configured** settings and extensions

### Productivity
- **Zero setup time** - everything pre-installed
- **Automatic verification** of tool availability
- **Integrated workflow** with VS Code
- **Make commands** for common tasks

### Quality Assurance
- **All quality tools** pre-installed and configured
- **Pre-commit hooks** automatically set up
- **CI/CD compatibility** - same tools as GitHub Actions
- **Multi-version testing** with tox

## 🔧 Customization

### Adding Tools
To add new development tools:

1. **Update pyproject.toml** dev dependencies
2. **Rebuild container**: `docker-compose build`
3. **Update verification script** if needed

### VS Code Settings
Customize `.devcontainer/devcontainer.json` for:
- Additional VS Code extensions
- Custom settings and keybindings
- Port forwarding
- Environment variables

### Container Configuration
Modify `Dockerfile` or `docker-compose.yml` for:
- System package installations
- Environment variables
- Volume mounts
- Resource limits

## 🚨 Troubleshooting

### Container Build Issues
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Tool Not Found
```bash
# Verify tool installation
./scripts/verify-container.sh

# Reinstall dev dependencies
pip install -e .[dev]
```

### Pre-commit Issues
```bash
# Reinstall hooks
pre-commit install --install-hooks

# Clear cache
pre-commit clean
```

### VS Code DevContainer Issues
1. Install "Dev Containers" extension
2. Reload VS Code window
3. Use Command Palette: "Dev Containers: Rebuild Container"

## 📝 Next Steps

1. **Build the container**: `docker-compose build`
2. **Start development**: `docker-compose up -d && docker-compose exec pirrtools-dev bash`
3. **Verify setup**: `./scripts/verify-container.sh`
4. **Start coding**: All tools are ready to use!

The container provides a complete, verified development environment with all necessary tools for professional Python development! 🎉