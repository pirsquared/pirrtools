#!/bin/bash

# Development Tools Verification Script
# Checks that all modern development tools are properly installed and working

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Verifying pirrtools development environment...${NC}"
echo "=================================================="

# Test counter
passed=0
failed=0

test_tool() {
    local tool_name="$1"
    local test_command="$2"
    local description="$3"
    
    echo -n "Testing $tool_name... "
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC} - $description"
        ((passed++))
    else
        echo -e "${RED}❌ FAIL${NC} - $description"
        ((failed++))
    fi
}

# Python and core tools
test_tool "Python" "python --version" "Python interpreter"
test_tool "pip" "pip --version" "Package installer"

# Testing tools
test_tool "pytest" "pytest --version" "Testing framework"
test_tool "pytest-cov" "python -c 'import pytest_cov'" "Test coverage"
test_tool "pytest-xdist" "python -c 'import xdist'" "Parallel testing"
test_tool "pytest-mock" "python -c 'import pytest_mock'" "Mocking utilities"

# Code quality tools
test_tool "black" "black --version" "Code formatter"
test_tool "isort" "isort --version" "Import sorter"
test_tool "ruff" "ruff --version" "Modern linter"
test_tool "mypy" "mypy --version" "Type checker"
test_tool "bandit" "bandit --version" "Security scanner"

# Development tools
test_tool "pre-commit" "pre-commit --version" "Git hooks manager"
test_tool "tox" "tox --version" "Testing automation"
test_tool "nox" "nox --version" "Modern testing automation"
test_tool "hatch" "hatch --version" "Modern project manager"

# Documentation tools  
test_tool "sphinx" "sphinx-build --version" "Documentation generator"
test_tool "sphinx-copybutton" "python -c 'import sphinx_copybutton'" "Sphinx copy buttons"

# Build tools
test_tool "build" "python -m build --version" "Package builder"
test_tool "twine" "twine --version" "PyPI uploader"
test_tool "wheel" "python -c 'import wheel'" "Wheel format support"

# Development utilities
test_tool "rich" "python -c 'import rich'" "Rich terminal library"
test_tool "ipython" "ipython --version" "Enhanced Python shell"
test_tool "jupyter" "jupyter --version" "Jupyter notebook"

# pirrtools specific tests
echo ""
echo -e "${BLUE}🎯 Testing pirrtools installation...${NC}"

test_tool "pirrtools" "python -c 'import pirrtools'" "Core pirrtools module"
test_tool "pirrtools.pandas" "python -c 'import pirrtools.pandas'" "Pandas utilities"
test_tool "pirrtools.structures" "python -c 'import pirrtools.structures'" "Data structures"

# Test .pirr accessor
echo -n "Testing .pirr accessor... "
if python -c "import pandas as pd; import pirrtools; df = pd.DataFrame({'a': [1,2,3]}); df.pirr" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC} - Pandas accessor registered"
    ((passed++))
else
    echo -e "${RED}❌ FAIL${NC} - Pandas accessor not working"
    ((failed++))
fi

# Final summary
echo ""
echo "=================================================="
echo -e "${BLUE}📊 Test Summary:${NC}"
echo -e "  ${GREEN}✅ Passed: $passed${NC}"
echo -e "  ${RED}❌ Failed: $failed${NC}"

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 All development tools are working correctly!${NC}"
    echo -e "${BLUE}🚀 Your development environment is ready!${NC}"
    exit 0
else
    echo -e "${RED}💥 Some tools failed verification. Please check the installation.${NC}"
    exit 1
fi