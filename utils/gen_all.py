#!/usr/bin/env python3
"""
综合脚本：接收用户输入，调用 gen_prompt.py 生成提示词，然后调用 gen_images.py 生成图像
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def run_gen_prompt(user_description: str, negative_requirements: str = ""):
    """
    运行 gen_prompt.py 生成 prompt.json 文件
    
    Args:
        user_description: 用户对图像的描述
        negative_requirements: 用户指定的负面要求
        
    Returns:
        bool: 是否成功生成 prompt.json
    """
    print("🎨 正在生成提示词...")
    
    try:
        if negative_requirements:
            cmd = [sys.executable, "gen_prompt.py", user_description, negative_requirements]
        else:
            cmd = [sys.executable, "gen_prompt.py", user_description]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ 提示词生成成功！")
            # Print the output from gen_prompt for user to see
            print(result.stdout)
            return True
        else:
            print(f"❌ 提示词生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 运行 gen_prompt.py 时出错: {e}")
        return False


def run_gen_images():
    """
    运行 gen_images.py 生成图像
    
    Returns:
        bool: 是否成功生成图像
    """
    print("🖼️ 正在生成图像...")
    
    try:
        cmd = [sys.executable, "gen_images.py"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ 图像生成成功！")
            print(result.stdout)
            return True
        else:
            print(f"❌ 图像生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 运行 gen_images.py 时出错: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🎨 综合生成工具：生成像素艺术图像")
    print("=" * 60)
    
    # 获取用户输入
    if len(sys.argv) > 1:
        user_description = sys.argv[1]
        negative_requirements = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        user_description = input("请输入您想要生成的像素画描述: ")
        negative_requirements = input("请输入您不希望出现的内容(可选，多个内容用逗号分隔): ")
    
    if not user_description:
        user_description = "simple game character"
    
    print(f"\n📝 描述: {user_description}")
    if negative_requirements:
        print(f"🚫 不希望出现: {negative_requirements}")
    
    # 步骤1: 生成提示词
    if not run_gen_prompt(user_description, negative_requirements):
        print("❌ 提示词生成失败，程序退出。")
        sys.exit(1)
    
    # 检查是否生成了 prompt.json
    prompt_file = Path("prompt.json")
    if not prompt_file.exists():
        print("❌ 未生成 prompt.json 文件，程序退出。")
        sys.exit(1)
    
    # 读取并显示生成的提示词
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)
        
        print(f"\n📋 生成的正面提示词:\n{prompt_data.get('positive', '')}")
        print(f"\n📋 生成的负面提示词:\n{prompt_data.get('negative', '')}")
        print(f"⚙️  生成参数: 步数={prompt_data.get('steps', 8)}, CFG={prompt_data.get('cfg', 10)}")
    except Exception as e:
        print(f"⚠️  读取 prompt.json 时出错: {e}")
    
    # 步骤2: 生成图像
    if not run_gen_images():
        print("❌ 图像生成失败，程序退出。")
        sys.exit(1)
    
    print("\n🎉 所有步骤完成！图像已保存到 generated_images 目录。")


if __name__ == "__main__":
    main()