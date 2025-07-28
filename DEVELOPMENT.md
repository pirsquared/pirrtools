# Development Guide

This document outlines the development workflow and tools available for pirrtools.

## Quick Start

### Option 1: Container Development (Recommended)
```bash
# Build and start the development container
docker-compose up -d

# Enter the container (all tools pre-installed)
docker-compose exec pirrtools-dev bash

# Container automatically sets up everything!
```

See [CONTAINER.md](CONTAINER.md) for detailed container documentation.

### Option 2: Local Development
```bash
# Install in development mode with all dev dependencies
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest

# Run all quality checks
pre-commit run --all-files
```

## Available Development Tools

### Testing
- **pytest**: Main testing framework
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution
- **tox**: Testing across multiple Python versions

```bash
# Run tests with coverage
pytest --cov=pirrtools --cov-report=term-missing

# Run tests in parallel
pytest -n auto

# Test across Python versions
tox
```

### Code Quality
- **black**: Code formatting (88 character line length)
- **isort**: Import sorting
- **flake8**: Style checking and linting
- **mypy**: Type checking
- **pylint**: Additional linting
- **bandit**: Security vulnerability scanning

```bash
# Format code
black pirrtools/ tests/

# Sort imports
isort pirrtools/ tests/

# Check style
flake8 pirrtools/ tests/

# Type checking
mypy pirrtools/

# Security scan
bandit -r pirrtools/
```

### Documentation
- **sphinx**: Documentation generation
- **sphinx-rtd-theme**: ReadTheDocs theme
- **sphinx-autodoc-typehints**: Automatic type hint documentation
- **myst-parser**: Markdown support in Sphinx

```bash
# Build documentation
cd docs/
make html
```

### Building and Publishing
- **build**: Modern Python package building
- **twine**: PyPI package uploading
- **wheel**: Wheel package format support

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (with proper authentication)
twine upload dist/*
```

## Pre-commit Hooks

The following hooks run automatically on each commit:

1. **trailing-whitespace**: Remove trailing whitespace
2. **end-of-file-fixer**: Ensure files end with newline
3. **check-yaml**: Validate YAML files
4. **check-added-large-files**: Prevent large files
5. **check-merge-conflict**: Detect merge conflicts
6. **debug-statements**: Find debug statements
7. **black**: Code formatting
8. **isort**: Import sorting
9. **flake8**: Style checking
10. **mypy**: Type checking
11. **bandit**: Security scanning

## CI/CD Pipeline

### GitHub Actions Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`):
   - Tests across Python 3.8-3.11
   - Code quality checks
   - Coverage reporting
   - Package building validation

2. **Documentation** (`.github/workflows/docs.yml`):
   - Builds Sphinx documentation
   - Deploys to GitHub Pages

3. **Publishing** (`.github/workflows/publish.yml`):
   - Automated PyPI publishing on releases
   - Test PyPI support for testing

### Tox Environments

Available tox environments:

- `py38`, `py39`, `py310`, `py311`: Test on different Python versions
- `lint`: Run all linting tools
- `mypy`: Type checking only

```bash
# Run specific environment
tox -e py311

# Run linting only
tox -e lint

# Run on all environments
tox
```

## Configuration Files

- **pyproject.toml**: Main project configuration
- **setup.cfg**: Additional tool configuration (flake8)
- **.pre-commit-config.yaml**: Pre-commit hook configuration
- **pytest.ini**: Pytest configuration
- **.github/workflows/**: CI/CD pipeline definitions

## Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**:
   - Write code following project conventions
   - Add tests for new functionality
   - Update documentation if needed

3. **Run Quality Checks**:
   ```bash
   pre-commit run --all-files
   pytest
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Add new feature"
   # Pre-commit hooks run automatically
   ```

5. **Push and Create PR**:
   ```bash
   git push origin feature/my-feature
   # Create PR on GitHub
   # CI pipeline runs automatically
   ```

## Code Quality Standards

- **Line Length**: 88 characters (Black standard)
- **Import Sorting**: isort with Black profile
- **Type Hints**: Encouraged but not required
- **Test Coverage**: Aim for >85% coverage
- **Documentation**: All public APIs should be documented
- **Security**: No high or medium severity bandit issues

## Troubleshooting

### Pre-commit Issues
```bash
# Skip hooks temporarily
git commit --no-verify

# Update hook versions
pre-commit autoupdate

# Clear cache
pre-commit clean
```

### Test Issues
```bash
# Run specific test
pytest tests/test_specific.py::test_function

# Debug failing test
pytest --pdb tests/test_specific.py::test_function

# Run without coverage
pytest --no-cov
```

### Type Checking Issues
```bash
# Run mypy with detailed output
mypy pirrtools/ --show-error-codes --show-error-context
```