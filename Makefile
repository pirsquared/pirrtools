# Makefile for pirrtools development

.PHONY: help install test lint format clean build publish docs container verify-container

# Default target
help:
	@echo "🛠️  pirrtools Development Commands"
	@echo "================================="
	@echo ""
	@echo "📦 Setup:"
	@echo "  install          Install package in development mode"
	@echo "  install-hooks    Install pre-commit hooks"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test             Run all tests"
	@echo "  test-cov         Run tests with coverage report"
	@echo "  test-fast        Run tests in parallel"
	@echo "  tox              Run tests across Python versions"
	@echo ""  
	@echo "🔍 Code Quality:"
	@echo "  lint             Run all linting tools"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run mypy type checking"
	@echo "  security         Run bandit security scan"
	@echo "  pre-commit       Run all pre-commit hooks"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs             Build Sphinx documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "📦 Building:"
	@echo "  build            Build wheel and source distribution"
	@echo "  clean            Clean build artifacts"
	@echo ""
	@echo "🐳 Container:"
	@echo "  container        Build development container"
	@echo "  container-run    Run development container"
	@echo "  verify-container Verify container setup"
	@echo ""

# Installation
install:
	@echo "📦 Installing pirrtools in development mode..."
	pip install -e .[dev]

install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install --install-hooks

# Testing
test:
	@echo "🧪 Running tests..."
	pytest tests/

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=pirrtools --cov-report=term-missing --cov-report=html

test-fast:
	@echo "🧪 Running tests in parallel..."
	pytest -n auto tests/

tox:
	@echo "🧪 Running tests across Python versions..."
	tox

# Code Quality
lint:
	@echo "🔍 Running all linting tools..."
	@echo "  Running flake8..."
	flake8 pirrtools/ tests/
	@echo "  Running pylint..."
	pylint pirrtools/
	@echo "  Running mypy..."
	mypy pirrtools/ --ignore-missing-imports
	@echo "  Running bandit..."
	bandit -r pirrtools/ --skip B101,B601
	@echo "✅ All linting checks passed!"

format:
	@echo "🎨 Formatting code..."
	black pirrtools/ tests/
	isort pirrtools/ tests/
	@echo "✅ Code formatted!"

type-check:
	@echo "🔍 Running type checking..."
	mypy pirrtools/ --ignore-missing-imports

security:
	@echo "🔒 Running security scan..."
	bandit -r pirrtools/ --skip B101,B601

pre-commit:
	@echo "🪝 Running pre-commit hooks..."
	pre-commit run --all-files

# Documentation
docs:
	@echo "📚 Building documentation..."
	cd docs && make html
	@echo "📖 Documentation built in docs/_build/html/"

docs-serve:
	@echo "📚 Serving documentation..."
	cd docs/_build/html && python -m http.server 8000

# Building
build:
	@echo "📦 Building package..."
	python -m build
	@echo "✅ Package built in dist/"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned!"

# Container
container:
	@echo "🐳 Building development container..."
	docker-compose build

container-run:
	@echo "🐳 Running development container..."
	docker-compose up -d
	docker-compose exec pirrtools-dev /bin/bash

verify-container:
	@echo "🔍 Verifying container setup..."
	./scripts/verify-container.sh

# Publishing (use with caution)
publish-test:
	@echo "📤 Publishing to Test PyPI..."
	@echo "⚠️  Make sure you have TEST_PYPI_API_TOKEN set"
	twine upload --repository testpypi dist/*

publish:
	@echo "📤 Publishing to PyPI..."
	@echo "⚠️  Make sure you have PYPI_API_TOKEN set"
	@echo "⚠️  This will publish to production PyPI!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	twine upload dist/*

# Development workflow
dev-setup: install install-hooks
	@echo "🎉 Development environment setup complete!"

dev-check: format lint test
	@echo "🎉 All development checks passed!"

dev-full: clean dev-setup dev-check build
	@echo "🎉 Full development cycle complete!"