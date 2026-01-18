'''
在当前文件中实现以下需求
1. 调用 lm studio 的模型 zai-org/glm-4.6v-flash 来生成 stable diffusion 的提示词
2. 生成的为高质量像素画，要求背景一定要纯白的，不要有杂色，阴影，边框，主体内容要严格符合用户要求，不要有多余的元素，要精确体现用户要求的内容
3. 主要用途是游戏素材
'''


import os
import json
import re
import requests
from typing import Dict, Any
import datetime


def save_prompts_to_template(positive_prompt: str, negative_prompt: str, filename: str = "prompt.json"):
    """
    将生成的正向和负向提示词保存到模板文件中
    
    Args:
        positive_prompt: 正向提示词
        negative_prompt: 负向提示词
        filename: 保存的文件名
    """
    # 读取模板文件
    template_path = os.path.join(os.path.dirname(__file__), "prompt.tpl")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_data = json.load(f)
    
    # 更新模板中的字段
    template_data["positive"] = positive_prompt
    template_data["negative"] = negative_prompt
    
    # 生成带时间戳的文件名
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_filename = f"prompt_{timestamp}.json"
    
    # 保存到新的JSON文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=4, ensure_ascii=False)
    
    print(f"提示词已保存到: {filename}")


def generate_stable_diffusion_prompt(user_description: str, negative_requirements: str = "") -> tuple[str, str]:
    """
    调用 LM Studio 模型 zai-org/glm-4.6v-flash 生成 Stable Diffusion 提示词
    
    Args:
        user_description: 用户对图像的描述
        negative_requirements: 用户指定的负面要求
        
    Returns:
        元组，包含优化后的正面提示词和负面提示词
    """
    # LM Studio 服务的基础 URL
    base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234")
    
    # 构建系统提示，强调返回纯净的提示词
    system_prompt = (
        "You are an expert at creating prompts for Stable Diffusion. "
        "Return ONLY two English prompts separated by '|||' - first the positive prompt for pixel art with a pure white background and no shadows, then the negative prompt. "
        "Do not include any explanations, thoughts, or metadata. "
        "Focus on clear, descriptive terms for high-quality pixel art suitable for game assets. "
        "Ensure no shadows appear in the generated image. "
        "Negative prompt should include: blurry, noisy, malformed text, watermark, logo, text, deformed, ugly, disfigured, bad eyes, crossed eyes, fused fingers, missing limbs, extra limbs, poorly drawn hands, poorly drawn feet, extra digits, fewer digits, gross proportions, signature, username, artist name. "
    )
    
    # 用户输入的描述
    if negative_requirements:
        user_prompt = f"Generate a concise English Stable Diffusion positive prompt and negative prompt for this pixel art game asset: {user_description}. Positive prompt must have white background, no shadows, and no borders. Negative prompt must include these specific requirements: {negative_requirements}. Separate the positive and negative prompts with '|||'. Output ONLY the prompts, no explanations."
    else:
        user_prompt = f"Generate a concise English Stable Diffusion positive prompt and negative prompt for this pixel art game asset: {user_description}. Positive prompt must have white background, no shadows, and no borders. Separate the positive and negative prompts with '|||'. Output ONLY the prompts, no explanations."
    
    # 准备请求数据
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        # "model": "zai-org/glm-4.6v-flash",
        "model": "qwen2.5-coder-7b-instruct-mlx",
        "temperature": 0.3,  # Even lower temperature for more deterministic output
        "max_tokens": None,  # No limit on output length
        "stream": False
    }
    
    try:
        # 发送请求到 LM Studio
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_content = result['choices'][0]['message']['content'].strip()
            
            # Look for "Thought:" marker and extract content after it
            thought_split = generated_content.split("Thought:")
            if len(thought_split) > 1:
                # Take the content after the last occurrence of "Thought:"
                generated_content = thought_split[-1].strip()
            
            # Split the content into positive and negative prompts if separator is present
            if "|||" in generated_content:
                parts = generated_content.split("|||")
                positive_prompt = parts[0].strip()
                negative_prompt = parts[1].strip() if len(parts) > 1 else ""
            else:
                # Fallback: treat all as positive prompt and use default negative prompt
                positive_prompt = generated_content
                negative_prompt = "blurry, noisy, malformed text, watermark, logo, text, deformed, ugly, disfigured, bad eyes, crossed eyes, fused fingers, missing limbs, extra limbs, poorly drawn hands, poorly drawn feet, extra digits, fewer digits, gross proportions, signature, username, artist name"
            
            # Process positive prompt
            # Use regex to extract the actual prompt from the response
            # Look for the actual prompt among potential explanations or thoughts
            # Common patterns: text between quotes, or after "Prompt:" or similar markers
            
            # First, try to find content in quotes
            quote_match = re.search(r'["“”](.+?)["“”]', positive_prompt)
            if quote_match:
                positive_prompt = quote_match.group(1).strip()
            else:
                # Look for content after indicators like "Output:" or "Result:"
                indicator_match = re.search(r'(?:Output|Result|Prompt|Response)[:\s]+(.+?)(?:\n|$)', positive_prompt, re.IGNORECASE)
                if indicator_match:
                    positive_prompt = indicator_match.group(1).strip()
                else:
                    # Extract the most likely prompt part - first sentence or paragraph
                    # Split by common separator lines and take the most relevant part
                    lines = [line.strip() for line in positive_prompt.split('\n') if line.strip()]
                    
                    # Filter out lines that are clearly explanatory
                    filtered_lines = []
                    for line in lines:
                        if not (line.lower().startswith(('here', 'the', 'this', 'thought')) or 
                                'prompt' in line.lower() or 
                                'result' in line.lower() or
                                'output' in line.lower() or
                                'response' in line.lower()):
                            filtered_lines.append(line)
                    
                    # Take the first substantial line that looks like a prompt
                    if filtered_lines:
                        positive_prompt = '. '.join(filtered_lines)
                    
            # Ensure the positive prompt is in English and contains essential pixel art elements
            if "pixel art" not in positive_prompt.lower():
                positive_prompt = f"pixel art style, {positive_prompt}"
            
            if "white background" not in positive_prompt.lower():
                positive_prompt += ", white background, no shadow, no border"
            elif "no shadow" not in positive_prompt.lower():
                # If white background is there but no shadow isn't mentioned
                positive_prompt += ", no shadow"
            
            # Clean up any double commas or spaces in positive prompt
            positive_prompt = positive_prompt.replace("  ", " ").replace(",,", ",").strip()
            
            # Clean up negative prompt
            negative_prompt = negative_prompt.replace("  ", " ").replace(",,", ",").strip()
            
            # Add user-specified negative requirements to the negative prompt
            if negative_requirements:
                # Ensure the negative requirements are added to the negative prompt
                negative_elements = [neg.strip() for neg in negative_requirements.split(',') if neg.strip()]
                for element in negative_elements:
                    if element.lower() not in negative_prompt.lower():
                        if negative_prompt:
                            negative_prompt += ", " + element
                        else:
                            negative_prompt = element
            
            # Add terms to ensure no borders and no shadows in the generated image
            if 'border' not in negative_prompt.lower():
                if negative_prompt:
                    negative_prompt += ", border, frame, outline"
                else:
                    negative_prompt = "border, frame, outline"
            
            if 'shadow' not in negative_prompt.lower():
                if negative_prompt:
                    negative_prompt += ", shadow, shade, shading"
                else:
                    negative_prompt = "shadow, shade, shading"
            
            return positive_prompt, negative_prompt
        else:
            print(f"Error from LM Studio: {response.status_code}, {response.text}")
            # 返回默认的正向和负向提示词
            positive_prompt = f"pixel art style, game asset, {user_description}, white background, no shadow, no border"
            negative_prompt = "blurry, noisy, malformed text, watermark, logo, text, deformed, ugly, disfigured, bad eyes, crossed eyes, fused fingers, missing limbs, extra limbs, poorly drawn hands, poorly drawn feet, extra digits, fewer digits, gross proportions, signature, username, artist name"
            
            # Add user-specified negative requirements to the negative prompt
            if negative_requirements:
                # Ensure the negative requirements are added to the negative prompt
                negative_elements = [neg.strip() for neg in negative_requirements.split(',') if neg.strip()]
                for element in negative_elements:
                    if element.lower() not in negative_prompt.lower():
                        if negative_prompt:
                            negative_prompt += ", " + element
                        else:
                            negative_prompt = element
            
            # Add terms to ensure no borders and no shadows in the generated image
            if 'border' not in negative_prompt.lower():
                if negative_prompt:
                    negative_prompt += ", border, frame, outline"
                else:
                    negative_prompt = "border, frame, outline"
            
            if 'shadow' not in negative_prompt.lower():
                if negative_prompt:
                    negative_prompt += ", shadow, shade, shading"
                else:
                    negative_prompt = "shadow, shade, shading"
            
            return positive_prompt, negative_prompt
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LM Studio: {e}")
        # 如果连接失败，返回一个基本的提示词
        positive_prompt = f"pixel art style, game asset, {user_description}, white background, no shadow, no border"
        negative_prompt = "blurry, noisy, malformed text, watermark, logo, text, deformed, ugly, disfigured, bad eyes, crossed eyes, fused fingers, missing limbs, extra limbs, poorly drawn hands, poorly drawn feet, extra digits, fewer digits, gross proportions, signature, username, artist name"
        
        # Add user-specified negative requirements to the negative prompt
        if negative_requirements:
            # Ensure the negative requirements are added to the negative prompt
            negative_elements = [neg.strip() for neg in negative_requirements.split(',') if neg.strip()]
            for element in negative_elements:
                if element.lower() not in negative_prompt.lower():
                    if negative_prompt:
                        negative_prompt += ", " + element
                    else:
                        negative_prompt = element
        
        # Add terms to ensure no borders and no shadows in the generated image
        if 'border' not in negative_prompt.lower():
            if negative_prompt:
                negative_prompt += ", border, frame, outline"
            else:
                negative_prompt = "border, frame, outline"
        
        if 'shadow' not in negative_prompt.lower():
            if negative_prompt:
                negative_prompt += ", shadow, shade, shading"
            else:
                negative_prompt = "shadow, shade, shading"
        
        return positive_prompt, negative_prompt


def main():
    """
    主函数，用于测试生成提示词的功能
    """
    # 获取用户输入或从命令行参数中获取
    import sys
    
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        # Check if there's a second argument for negative requirements
        negative_req = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        user_input = input("请输入您想要生成的像素画描述: ")
        negative_req = input("请输入您不希望出现的内容(可选，多个内容用逗号分隔): ")
    
    if not user_input:
        user_input = "simple game character"
    positive_prompt, negative_prompt = generate_stable_diffusion_prompt(user_input, negative_req)
    print(f"\n生成的 Stable Diffusion 正面提示词:\n{positive_prompt}")
    print(f"\n生成的 Stable Diffusion 负面提示词:\n{negative_prompt}")
    
    # 保存提示词到模板文件
    save_prompts_to_template(positive_prompt, negative_prompt)


if __name__ == "__main__":
    main()
