# Makefile for Pixel Art Generator

.PHONY: install run test clean help

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  run        - Run the development server"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean generated files"

install:
	pip install -r requirements.txt

run:
	python api/main.py

test:
	pytest tests/

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete