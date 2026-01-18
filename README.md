# Pixel Art Generator

A web-based tool for generating pixel art images using AI. The application allows users to input text descriptions and generates corresponding pixel art with customizable parameters.

## Features

- 🎨 Web interface for easy image generation
- 🖼️ Support for both positive and negative prompts
- ⚙️ Configurable generation parameters (steps, CFG scale)
- 📋 View generated prompts directly in the UI
- 🎯 Optimized for game asset creation

## Architecture

- **Frontend**: HTML/CSS/JavaScript served via Flask
- **Backend**: Python Flask API
- **Image Generation**: Integration with Draw Things API
- **Prompt Generation**: AI-powered prompt creation

## Project Structure

```
pixel-art-generator/
├── api/                           # Backend API implementation
│   ├── __init__.py               # Package initialization
│   └── main.py                   # Main Flask application
├── frontend/                      # Frontend assets
│   ├── __init__.py               # Package initialization
│   └── index.html                # Main HTML page
├── utils/                         # Utility scripts
│   ├── __init__.py               # Package initialization
│   ├── gen_all.py                # Orchestrates the generation process
│   ├── gen_prompt.py             # Generates image prompts
│   └── gen_images.py             # Generates images from prompts
├── docs/                          # Documentation
│   └── README.md                 # Project documentation
├── tests/                         # Test files
│   └── test_app.py               # Application tests
├── config.py                     # Centralized configuration management
├── generated_images/              # Output directory for generated images
├── utils/prompt.tpl              # Template for prompt generation
├── .env.example                  # Environment variable examples
├── .gitignore                    # Git ignore rules
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── setup.py                      # Package setup configuration
├── Makefile                      # Common development tasks
├── package.json                  # Node.js package manifest
├── LICENSE                       # License information
└── README.md                     # This file
```

## Setup

1. Clone the repository from https://github.com/kevinlights/pixel-art-generator.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment example and configure your settings:
   ```bash
   cp .env.example .env
   # Edit .env to match your local configuration
   ```
4. Ensure LM Studio is running with the required model (configured in .env)
5. Ensure Draw Things API is running on the configured endpoint (default: http://localhost:7860)
6. Run the application:
   ```bash
   python api/main.py
   ```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize the settings:

- `LM_STUDIO_BASE_URL`: Base URL for LM Studio API (default: http://localhost:1234)
- `LM_STUDIO_MODEL`: Model to use for prompt generation
- `DRAW_THINGS_API_URL`: API endpoint for image generation (default: http://localhost:7860/sdapi/v1/txt2img)
- `DEFAULT_STEPS`, `DEFAULT_CFG`: Default image generation parameters
- `GENERATED_IMAGES_DIR`: Directory for saving generated images
- `PROMPT_TEMPLATE_PATH`: Path to the prompt template file

## Usage

1. Start the server
2. Navigate to `http://localhost:5001`
3. Enter a description for the pixel art you want to generate
4. Optionally specify elements to avoid in the negative prompt
5. Click "Generate Pixel Art"
6. View the generated image and prompts in the UI

## Dependencies

### Software Dependencies
- Python 3.8+
- Flask
- requests
- Pillow
- python-dotenv (for configuration management)

### External Services
- LM Studio with compatible model (e.g., qwen2.5-coder-7b-instruct-mlx)
- Draw Things API (or compatible Stable Diffusion API endpoint)

### Configuration
All services are configurable via environment variables in a `.env` file (see `.env.example` for defaults).

## Development

The project includes development tools and scripts:

- `make test`: Run the test suite
- `make run`: Run the development server
- `make install`: Install dependencies
- `make clean`: Clean generated files

Development dependencies can be installed with:
```bash
pip install -r requirements-dev.txt
```

## License

MIT License - See LICENSE file for details.