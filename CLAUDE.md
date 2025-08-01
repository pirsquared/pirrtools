# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Session Context

For context from previous conversations and changes made to this codebase, see [CONVERSATION_LOG.md](CONVERSATION_LOG.md). This log maintains a chronological record of discussions, decisions, and modifications across development sessions.

## Development Commands

### Testing
- Run all tests: `pytest`
- Run with coverage: `pytest --cov=pirrtools`
- Run specific test: `pytest tests/test_pandas.py::test_simple_dataframe`

### Code Quality
- Format code: `black pirrtools tests`
- Run modern linter: `ruff check pirrtools tests`
- Run type checker: `mypy pirrtools`
- Pre-commit hooks: `pre-commit run --all-files`

### Documentation
- Build Sphinx docs: `make -C docs html`
- Serve docs locally: `python -m http.server 8080 --directory docs/_build/html`
- Interactive tutorial: `python examples/tutor.py`

### Building and Distribution
- Build package: `python -m build`
- Upload to PyPI: `twine upload dist/*`

### Development Installation

#### Local Installation
- Install in development mode: `pip install -e .`
- Install with dev dependencies: `pip install -e .[dev]`

Note: Modern pip (>=21.3) supports editable installs directly from pyproject.toml without requiring setup.py.

#### Docker Container Development
For consistent development environments:

```bash
# Build and run development container
docker-compose up -d
docker-compose exec pirrtools-dev bash

# Or run commands directly
docker-compose run --rm pirrtools-dev pytest
docker-compose run --rm pirrtools-dev black pirrtools tests
```

**VS Code Dev Container**: Open the project in VS Code and select "Reopen in Container" when prompted, or use Command Palette > "Dev Containers: Reopen in Container".

## Architecture Overview

### Core Modules

**pirrtools/__init__.py**
- Main entry point exposing key functionality
- Contains utility functions: `addpath()`, `reload_entity()`, `find_instances()`
- Handles loading of `.pirc` configuration files from home directory
- Automatically sets up matplotlib inline for IPython environments

**pirrtools/pandas.py**
- Core caching functionality using feather format for pandas objects
- Provides `UtilsAccessor` class registered as `.pirr` accessor on DataFrames/Series
- Key functions: `_save_cache()`, `load_cache()`, `cache_and_load()`
- Handles complex pandas objects including MultiIndex and Series with custom names
- Creates dynamic groupby accessors (`i0`, `i1`) for different index levels

**pirrtools/structures/attrpath.py**
- Enhanced pathlib.Path subclass with attribute-based navigation
- Provides intelligent file viewing based on file extensions (HTML, SVG, images, CSV, etc.)
- Syntax highlighting for code files using Pygments
- Directory contents accessible as attributes with safe naming conventions
- Organizes files by type (directories in `.D`, files in `.F`, by extension)

**pirrtools/structures/attrdict.py**
- Dictionary with attribute access capabilities
- Foundation for AttrPath's attribute-based file system navigation

### Key Features

1. **Pandas Caching System**: Primary feature allowing caching of non-conforming datasets using feather format
2. **AttrPath Navigation**: File system navigation using dot notation with intelligent file viewing
3. **IPython Integration**: Automatic matplotlib setup and custom display handlers
4. **Development Utilities**: Module reloading, path management, instance finding

### Configuration Files

- **pyproject.toml**: Primary configuration with build system, dependencies, and tool settings
- **pytest.ini**: Test configuration with warning filters
- **Black**: Line length 88, Python 3.8+ target, specific exclusions configured
- **Dockerfile**: Python 3.11 development container with all dev dependencies
- **docker-compose.yml**: Container orchestration for development
- **.devcontainer/**: VS Code development container configuration

### Testing Strategy

Tests are located in `tests/` directory with pytest framework. Key test files:
- `test_pandas.py`: Core caching functionality tests  
- `test_to_rich.py`: Comprehensive to_rich method testing (177 tests)
- `test_structures.py`: AttrDict/AttrPath testing
- `test_init.py`: Integration and utility testing
- `test_list_chunks.py`: List chunking utilities
- `test_sequences.py`: Sequence manipulation functions

Tests use temporary directories (`tmp_path` fixture) and pandas testing utilities for DataFrame/Series comparisons. Current test coverage: 88% with comprehensive parameter testing and edge case validation.

## Pre-Commit/Push Checklist

Before committing or pushing changes, follow this checklist to ensure code quality and consistency:

### 1. Code Quality Checks
```bash
# Format code with Black
black pirrtools tests

# Sort imports with isort
isort pirrtools tests

# Run linter checks with flake8
flake8 pirrtools tests

# Run type checking
mypy pirrtools
```

### 2. Testing
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=pirrtools

# Verify no test failures or regressions
```

### 3. Documentation
```bash
# Build documentation (if docs were modified)
make -C docs html

# Verify no build errors or warnings
# Check that Rich tables display properly in light theme
```

### 4. Pre-commit Hooks
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Fix any issues identified by hooks
```

### 5. Build Verification
```bash
# Build package to verify setup
python -m build

# Verify build completes without errors
```

### 6. Final Checks
- [ ] All tests passing
- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No linting errors from flake8
- [ ] No type checking errors from mypy
- [ ] Documentation builds successfully (if modified)
- [ ] No debugging files or temporary code left in repository
- [ ] Commit message follows conventional format
- [ ] Version numbers updated if needed:
  - [ ] `pyproject.toml` version field (line 7)
  - [ ] `docs/conf.py` release field (line 18)

### 7. Commit Standards
- Use clear, descriptive commit messages
- Include context about what changed and why
- Reference any relevant issues or pull requests
- Follow conventional commit format when applicable

This checklist ensures consistent code quality and prevents common issues from reaching the main branch.