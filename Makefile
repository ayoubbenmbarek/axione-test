.PHONY: help install dev run test coverage lint format typecheck clean all

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Install dev dependencies and setup"
	@echo "  make run        - Run the API server"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make lint       - Run linter (ruff)"
	@echo "  make format     - Format code (ruff)"
	@echo "  make typecheck  - Run type checker (mypy)"
	@echo "  make clean      - Remove cache files"
	@echo "  make all        - Run lint, typecheck, and tests"

# Install dependencies
install:
	pip install -r requirements.txt

# Install with dev setup
dev:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Run 'source venv/bin/activate' to activate the virtual environment"

# Run the API server
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest -v

# Run tests with coverage
coverage:
	pytest --cov=app --cov-report=term-missing --cov-report=html
	@echo "HTML report generated in htmlcov/index.html"

# Lint code
lint:
	ruff check app tests

# Format code
format:
	ruff format app tests
	ruff check --fix app tests

# Type checking
typecheck:
	mypy app --ignore-missing-imports

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "Cleaned cache files"

# Run all checks
all: lint typecheck test
	@echo "All checks passed!"
