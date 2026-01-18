#!/usr/bin/env python3
"""
Web API server for generating pixel art images
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the app with config settings
Config.init_app(app)

# Directory for storing generated images
IMAGES_DIR = Config.GENERATED_IMAGES_DIR
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.route('/')
def index():
    """Serve the main HTML page"""
    # Get the directory where this main.py file is located
    main_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then look for frontend files
    root_dir = os.path.dirname(main_dir)
    index_path = os.path.join(root_dir, 'index.html')
    
    # If index.html doesn't exist in root, try the frontend directory
    if not os.path.exists(index_path):
        index_path = os.path.join(root_dir, 'frontend', 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(os.path.join(root_dir, 'frontend'), 'index.html')
        else:
            # Return a simple error page if index.html is not found
            return '<h1>Pixel Art Generator</h1><p>Index file not found. Check if frontend/index.html exists.</p>', 404
    
    return send_from_directory(root_dir, 'index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate an image based on user prompts"""
    try:
        data = request.get_json()
        
        # Extract prompts from the request
        user_description = data.get('prompt', '')
        negative_requirements = data.get('negative_prompt', '')
        
        if not user_description:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Import and run the generation functions directly
        print("Generating prompts and image...")
        try:
            # Import the required functions
            import sys
            import os
            utils_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils')
            sys.path.insert(0, utils_path)
                    
            from gen_prompt import generate_stable_diffusion_prompt, save_prompts_to_template
            from gen_images import load_prompt_from_json, call_draw_things_api, save_image
                    
            # Generate prompts
            positive_prompt, negative_prompt = generate_stable_diffusion_prompt(user_description, negative_requirements)
                    
            # Save prompts to template
            save_prompts_to_template(positive_prompt, negative_prompt, "prompt.json")
                    
            # Load the saved prompts to get all parameters
            positive_prompt, negative_prompt, steps, cfg = load_prompt_from_json("prompt.json")
                    
            # Generate image using the Draw Things API
            img = call_draw_things_api(
                prompt=positive_prompt,
                negative_prompt=negative_prompt,
                steps=steps,
                cfg=cfg
            )
                    
            if img is None:
                return jsonify({'error': 'Image generation failed - check if Draw Things API is running'}), 500
                    
            # Save the generated image
            save_image(img)  # Uses config-defined directory
                    
        except ImportError as e:
            print(f"Import error: {e}")
            return jsonify({'error': f'Import failed: {str(e)}'}), 500
        except Exception as e:
            print(f"Generation error: {e}")
            return jsonify({'error': f'Generation failed: {str(e)}'}), 500
        
        # Read the generated prompt.json to get the prompts
        # The file is created in the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_file = Path(project_root) / 'prompt.json'
        
        # Check if the file exists in project root first, otherwise check current directory
        if not prompt_file.exists():
            # Try to find it in the current directory
            prompt_file = Path('prompt.json')
        
        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            positive_prompt = prompt_data.get('positive', '')
            negative_prompt = prompt_data.get('negative', '')
            steps = prompt_data.get('steps', 8)
            cfg = prompt_data.get('cfg', 10)
        else:
            positive_prompt = ""
            negative_prompt = ""
            steps = 8
            cfg = 10
        
        # Find the most recently generated image
        # Use the configured image directory path
        image_files = []
        for ext in ['.png', '.jpg', '.jpeg']:
            image_files.extend(list(Path(IMAGES_DIR).glob(f'*{ext}')))
        
        if not image_files:
            return jsonify({'error': 'No image was generated'}), 500
            
        # Get the most recent image
        latest_image = max(image_files, key=lambda x: x.stat().st_mtime)
        image_filename = latest_image.name
        
        return jsonify({
            'success': True,
            'image_url': f'/images/{image_filename}',
            'image_filename': image_filename,
            'positive_prompt': positive_prompt,
            'negative_prompt': negative_prompt,
            'steps': steps,
            'cfg': cfg
        })
        
    except Exception as e:
        print(f"Exception in generate_image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/images/<filename>')
def serve_image(filename):
    """Serve generated images"""
    # Use absolute path for security
    abs_images_dir = os.path.abspath(IMAGES_DIR)
    return send_from_directory(abs_images_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)