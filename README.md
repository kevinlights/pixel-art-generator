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
├── api/                    # Backend API implementation
│   └── main.py            # Main Flask application
├── frontend/              # Frontend assets
│   └── index.html         # Main HTML page
├── utils/                 # Utility scripts
│   ├── gen_all.py         # Orchestrates the generation process
│   ├── gen_prompt.py      # Generates image prompts
│   └── gen_images.py      # Generates images from prompts
├── docs/                  # Documentation
├── tests/                 # Test files
├── generated_images/      # Output directory for generated images
├── prompt.tpl             # Template for prompt generation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

1. Clone the repository from https://github.com/kevinlights/pixel-art-generator.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure LM Studio is running with the `qwen2.5-coder-7b-instruct-mlx` model
4. Run the application:
   ```bash
   python api/main.py
   ```

## Usage

1. Start the server
2. Navigate to `http://localhost:5001`
3. Enter a description for the pixel art you want to generate
4. Optionally specify elements to avoid in the negative prompt
5. Click "Generate Pixel Art"
6. View the generated image and prompts in the UI

## Dependencies

- Python 3.8+
- Flask
- requests
- Pillow
- Draw Things API access

## License

MIT License - See LICENSE file for details.