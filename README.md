# Pixel Art Generator 🎨

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/kevinlights/pixel-art-generator)

A powerful web-based tool for generating pixel art images using AI. Create stunning retro-style game assets and pixel art with just a few clicks!

**✨ Why Pixel Art Generator?**
- **Fast**: Generate pixel art in seconds with LCM LoRA
- **Private**: 100% local processing, no data leaves your device
- **Customizable**: Fine-tune every aspect of your pixel art
- **Game Ready**: Perfect for indie game developers and pixel art enthusiasts

## Features

- 🎨 **Intuitive Web Interface**: Easy-to-use UI for generating pixel art with real-time feedback
- 🤖 **AI-Powered Prompt Generation**: Smart prompt creation using local LLMs via LM Studio
- 🎨 **Pixel Art Specialization**: Optimized with Pixel Art XL LoRA for authentic retro style
- ⚡ **Fast Inference**: LCM LoRA enables quick image generation without sacrificing quality
- 🖼️ **Dual Prompt Support**: Both positive and negative prompts for precise control
- ⚙️ **Configurable Parameters**: Adjust steps, CFG scale, and other generation settings
- 📋 **Prompt Visualization**: View generated prompts directly in the UI
- 🎯 **Game Asset Ready**: Outputs optimized for game development and indie projects
- 🔒 **Privacy-First**: All processing happens locally, no data sent to external services

## Architecture

- **Frontend**: Modern HTML/CSS/JavaScript interface served via Flask
- **Backend**: Python Flask API with RESTful endpoints
- **Prompt Generation**: AI-powered prompt creation using local LLMs (LM Studio)
- **Image Generation**: Stable Diffusion XL with specialized LoRAs:
  - **Pixel Art XL LoRA**: Authentic pixel art style (weight: 1.3)
  - **LCM LoRA**: Fast inference with minimal steps (weight: 1.0)
- **API Integration**: Draw Things app for local GPU acceleration

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
├── LICENSE                       # License information
└── README.md                     # This file
```

## Setup

### Prerequisites

1. **Python 3.8+** installed on your system
2. **LM Studio** with a compatible model (e.g., qwen2.5-coder-7b-instruct-mlx)
3. **Draw Things** app installed on your iOS/macOS device with the following models:
   - Base SDXL model
   - **Required LoRA Models** (must be imported into Draw Things):
     - `lcm_lora_sdxl_lora_f16.ckpt` (for fast inference)
     - `pixel_art_xl_lora_f16.ckpt` (for pixel art style)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/kevinlights/pixel-art-generator.git
   cd pixel-art-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to match your local configuration
   ```

4. Start LM Studio with your preferred model

5. In Draw Things app:
   - Enable **Remote API** in Settings
   - Note the API endpoint URL (default: http://localhost:7860)
   - Ensure both LoRA models are imported and available

6. Run the application:
   ```bash
   python api/main.py
   ```

7. Open your browser and navigate to:
   ```
   http://localhost:5001
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

### Basic Usage

1. Start the server:
   ```bash
   python api/main.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5001
   ```

3. Enter a description for your pixel art:
   - **Positive Prompt**: "A cute pixel art cat sitting on a rooftop, retro style, vibrant colors"
   - **Negative Prompt**: "blurry, modern, realistic, 3d render"

4. Click "Generate Pixel Art" and wait for the magic!

5. View the generated image and the AI-enhanced prompts in the UI

### Example Prompts

**Character Design:**
```
Pixel art warrior character, 16-bit style, holding a sword, fantasy theme, detailed armor, vibrant palette
```

**Game Environment:**
```
Pixel art forest scene, SNES style, parallax layers, day time, mushrooms, trees, path, cozy atmosphere
```

**Item/Prop:**
```
Pixel art potion bottle, 8-bit style, glowing blue liquid, cork stopper, magical effects, simple background
```

### Tips for Best Results

- **Be specific**: Include details like "16-bit style", "SNES era", or "Game Boy palette"
- **Use negative prompts**: Exclude modern elements like "3D render", "photorealistic", or "blurry"
- **Keep it concise**: Focus on 3-5 key elements for best results
- **Experiment**: Try different step counts (8-20) and CFG scales (7-12)

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