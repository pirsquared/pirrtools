#!/bin/bash

# Container Development Environment Verification Script
# This script verifies that all development tools are properly installed in the container

set -e

echo "🔍 Verifying pirrtools development container setup..."
echo "=================================================="

# Check Python and pip
echo "🐍 Checking Python environment..."
python --version
pip --version

# Check core development tools
echo ""
echo "🔧 Checking core development tools..."

tools=(
    "pytest:pytest --version"
    "black:black --version"
    "isort:isort --version"
    "flake8:flake8 --version"
    "mypy:mypy --version"
    "pre-commit:pre-commit --version"
    "tox:tox --version"
    "sphinx:sphinx-build --version"
    "build:python -m build --help"
    "twine:twine --version"
)

for tool_info in "${tools[@]}"; do
    tool_name=$(echo "$tool_info" | cut -d: -f1)
    tool_cmd=$(echo "$tool_info" | cut -d: -f2-)

    echo -n "  Checking $tool_name... "
    if $tool_cmd >/dev/null 2>&1; then
        echo "✅"
    else
        echo "❌"
        echo "    Command failed: $tool_cmd"
    fi
done

# Check Python imports
echo ""
echo "📦 Checking Python package imports..."

packages=(
    "pytest"
    "black"
    "isort"
    "flake8"
    "mypy"
    "tox"
    "sphinx"
    "pandas"
    "numpy"
    "rich"
    "matplotlib"
    "ipython"
    "jupyter"
)

for package in "${packages[@]}"; do
    echo -n "  Importing $package... "
    if python -c "import $package" 2>/dev/null; then
        echo "✅"
    else
        echo "❌"
    fi
done

# Check pirrtools installation
echo ""
echo "🛠️  Checking pirrtools installation..."
echo -n "  Installing pirrtools in development mode... "
if pip install -e . >/dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
fi

echo -n "  Importing pirrtools... "
if python -c "import pirrtools; print(f'pirrtools version: {getattr(pirrtools, \"__version__\", \"dev\")}')" 2>/dev/null; then
    echo "✅"
else
    echo "❌"
fi

# Check system tools
echo ""
echo "🖥️  Checking system tools..."

sys_tools=(
    "git:git --version"
    "node:node --version"
    "npm:npm --version"
    "jq:jq --version"
    "tree:tree --version"
    "curl:curl --version"
)

for tool_info in "${sys_tools[@]}"; do
    tool_name=$(echo "$tool_info" | cut -d: -f1)
    tool_cmd=$(echo "$tool_info" | cut -d: -f2-)

    echo -n "  Checking $tool_name... "
    if $tool_cmd >/dev/null 2>&1; then
        echo "✅"
    else
        echo "❌"
    fi
done

# Check configuration files
echo ""
echo "📋 Checking configuration files..."

config_files=(
    "pyproject.toml"
    "setup.cfg"
    ".pre-commit-config.yaml"
    "pytest.ini"
    ".github/workflows/ci.yml"
    ".github/workflows/publish.yml"
    ".github/workflows/docs.yml"
)

for file in "${config_files[@]}"; do
    echo -n "  Checking $file... "
    if [ -f "$file" ]; then
        echo "✅"
    else
        echo "❌"
    fi
done

# Run a quick test suite
echo ""
echo "🧪 Running quick test verification..."
echo -n "  Running pytest... "
if pytest tests/ -q --tb=no >/dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
fi

# Check pre-commit hooks
echo ""
echo "🪝 Checking pre-commit setup..."
echo -n "  Pre-commit hooks installed... "
if [ -d ".git/hooks" ] && [ -f ".git/hooks/pre-commit" ]; then
    echo "✅"
else
    echo "⚠️  (will be installed on first use)"
fi

echo ""
echo "🎉 Container verification complete!"
echo ""
echo "📚 Quick reference for development commands:"
echo "  pytest                    - Run tests"
echo "  pytest --cov=pirrtools    - Run tests with coverage"
echo "  black pirrtools/ tests/   - Format code"
echo "  isort pirrtools/ tests/   - Sort imports"
echo "  flake8 pirrtools/ tests/  - Check style"
echo "  mypy pirrtools/           - Type checking"
echo "  pre-commit run --all-files - Run all quality checks"
echo "  tox                       - Test across Python versions"
echo "  python -m build           - Build package"
echo ""
echo "🚀 Ready for development!"
