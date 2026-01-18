#!/usr/bin/env python3
"""
使用生成的 prompt.json 文件，调用 draw things 的 API 生成图像
"""

import requests
import json
import time
import base64
from io import BytesIO
from PIL import Image
from pathlib import Path
import os
import sys
import inspect

# Get the project root directory to import config
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from config import Config
    GENERATED_IMAGES_DIR = Config.GENERATED_IMAGES_DIR
    DRAW_THINGS_API_URL = getattr(Config, 'DRAW_THINGS_API_URL', 'http://localhost:7860/sdapi/v1/txt2img')
except ImportError:
    # Fallback to defaults if config is not available
    GENERATED_IMAGES_DIR = "generated_images"
    DRAW_THINGS_API_URL = 'http://localhost:7860/sdapi/v1/txt2img'


def load_prompt_from_json(json_file_path: str = "prompt.json"):
    """
    从 JSON 文件加载提示词
    
    Args:
        json_file_path: JSON 文件路径
        
    Returns:
        tuple: (positive_prompt, negative_prompt, steps, cfg)
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    positive_prompt = data.get("positive", "")
    negative_prompt = data.get("negative", "")
    steps = data.get("steps", 8)
    cfg = data.get("cfg", 10)
    
    return positive_prompt, negative_prompt, steps, cfg


def call_draw_things_api(prompt: str, negative_prompt: str, steps: int, cfg: float, 
                         width: int = 512, height: int = 512, seed: int = -1):
    """
    调用 Draw Things API 生成图像
    
    Args:
        prompt: 正向提示词
        negative_prompt: 负向提示词
        steps: 生成步数
        cfg: CFG 值
        width: 图像宽度
        height: 图像高度
        seed: 随机种子
        
    Returns:
        PIL.Image: 生成的图像对象，如果失败则返回 None
    """
    # Draw Things API 地址
    api_url = DRAW_THINGS_API_URL
    
    # 构建请求参数
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": "LCM",
        "seed": seed,
        "loras": [
            {
                "file": "lcm_lora_sdxl_lora_f16.ckpt",
                "weight": 1.0,
                "mode": "all"
            },
            {
                "file": "pixel_art_xl_lora_f16.ckpt",
                "weight": 1.3,
                "mode": "all"
            }
        ],
    }
    
    print(f"🔄 正在生成图像...")
    print(f"📝 正向提示词: {prompt[:100]}...")
    print(f"📝 负向提示词: {negative_prompt[:100]}...")
    print(f"⚙️  参数: 步数={steps}, CFG={cfg}, 尺寸={width}x{height}")
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=300  # 5分钟超时
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if "images" in result and len(result["images"]) > 0:
                # 解码 base64 图片数据
                img_data = base64.b64decode(result["images"][0])
                img = Image.open(BytesIO(img_data))
                
                print(f"✅ 图像生成成功！")
                return img
            else:
                print(f"❌ 响应中没有图片数据")
                print(f"响应内容: {result}")
                return None
        else:
            print(f"❌ API 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（超过 300 秒）")
        return None
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return None


def save_image(img: Image.Image, output_dir: str = None):
    """
    保存图像到指定目录
    
    Args:
        img: PIL 图像对象
        output_dir: 输出目录
    """
    # Use config value if output_dir is not provided
    if output_dir is None:
        output_dir = GENERATED_IMAGES_DIR
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 生成带时间戳的文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"generated_{timestamp}.png"
    filepath = output_path / filename
    
    # 保存图像
    img.save(filepath, format="PNG")
    print(f"💾 图像已保存到: {filepath}")


def main():
    """主函数"""
    print("=" * 60)
    print("🎨 使用 prompt.json 生成像素艺术图像")
    print("=" * 60)
    
    # 检查是否存在 prompt.json 文件
    if not os.path.exists("prompt.json"):
        print("❌ 未找到 prompt.json 文件")
        print("💡 请先运行 gen_prompt.py 生成提示词文件")
        return
    
    # 从 JSON 文件加载提示词
    print("📥 正在加载 prompt.json...")
    positive_prompt, negative_prompt, steps, cfg = load_prompt_from_json("prompt.json")
    
    print(f"📋 正向提示词: {positive_prompt}")
    print(f"📋 负向提示词: {negative_prompt}")
    print(f"⚙️  参数: 步数={steps}, CFG={cfg}")
    
    # 调用 Draw Things API 生成图像
    img = call_draw_things_api(
        prompt=positive_prompt,
        negative_prompt=negative_prompt,
        steps=steps,
        cfg=cfg
    )
    
    if img:
        # 保存图像到配置的目录
        save_image(img)
        print("🎉 图像生成完成！")
    else:
        print("❌ 图像生成失败，请检查 Draw Things 是否正在运行并启用了 API")


if __name__ == "__main__":
    main()