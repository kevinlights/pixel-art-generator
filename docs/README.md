# Pixel Art Generator Documentation

## Overview

The Pixel Art Generator is a web application that allows users to generate pixel art images from text descriptions using AI. The application consists of a web interface and backend services that communicate with AI models to generate appropriate prompts and images.

## Architecture

The application is built with a modular architecture:

- **Frontend**: HTML/CSS/JavaScript interface served via Flask
- **API Layer**: Flask backend handling requests and orchestrating generation
- **Utils**: Core functionality for prompt and image generation
- **Configuration**: Centralized settings management

## Components

### API Layer (`/api/`)

The main Flask application that serves the web interface and provides the image generation API endpoints.

### Utils (`/utils/`)

Contains the core functionality:

- `gen_prompt.py`: Generates positive and negative prompts from user descriptions
- `gen_images.py`: Calls the Draw Things API to generate images
- `gen_all.py`: Orchestrates the complete generation process

### Configuration (`config.py`)

Centralized configuration management with environment variable support.

## Running the Application

### Prerequisites

- Python 3.8+
- LM Studio with `qwen2.5-coder-7b-instruct-mlx` model running locally

### Installation

1. Clone the repository from https://github.com/kevinlights/pixel-art-generator.git
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and adjust settings as needed
4. Run the application: `python api/main.py`

## API Endpoints

### GET /
Serves the main HTML page

### POST /generate
Accepts JSON with `prompt` and `negative_prompt` fields, returns generated image URL and prompt information.

## Development

Run tests: `make test`
Install dev dependencies: `pip install -r requirements-dev.txt`