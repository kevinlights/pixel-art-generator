# Configuration for Pixel Art Generator

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # API settings
    LM_STUDIO_BASE_URL = os.environ.get('LM_STUDIO_BASE_URL') or 'http://localhost:1234'
    LM_STUDIO_MODEL = os.environ.get('LM_STUDIO_MODEL') or 'qwen2.5-coder-7b-instruct-mlx'
    DRAW_THINGS_API_URL = os.environ.get('DRAW_THINGS_API_URL') or 'http://localhost:7860/sdapi/v1/txt2img'
    
    # Image generation settings
    DEFAULT_STEPS = int(os.environ.get('DEFAULT_STEPS') or 8)
    DEFAULT_CFG = float(os.environ.get('DEFAULT_CFG') or 10.0)
    DEFAULT_WIDTH = int(os.environ.get('DEFAULT_WIDTH') or 512)
    DEFAULT_HEIGHT = int(os.environ.get('DEFAULT_HEIGHT') or 512)
    
    # File paths
    GENERATED_IMAGES_DIR = os.environ.get('GENERATED_IMAGES_DIR') or 'generated_images'
    PROMPT_TEMPLATE_PATH = os.environ.get('PROMPT_TEMPLATE_PATH') or os.path.join('utils', 'prompt.tpl')
    
    # Create directories if they don't exist
    @staticmethod
    def init_app(app):
        os.makedirs(Config.GENERATED_IMAGES_DIR, exist_ok=True)
        prompt_template_path = Config.PROMPT_TEMPLATE_PATH
        # Ensure the directory exists
        os.makedirs(os.path.dirname(prompt_template_path), exist_ok=True)
        
        if not os.path.exists(prompt_template_path):
            # Create a default prompt template if it doesn't exist
            default_template = {
                "positive": "",
                "negative": "",
                "steps": Config.DEFAULT_STEPS,
                "cfg": Config.DEFAULT_CFG,
                "width": Config.DEFAULT_WIDTH,
                "height": Config.DEFAULT_HEIGHT
            }
            import json
            with open(prompt_template_path, 'w', encoding='utf-8') as f:
                json.dump(default_template, f, indent=4, ensure_ascii=False)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}