#!/usr/bin/env python3
"""
Kindle Paperwhite 屏保转换工具
将 KPW1 格式 (758x1024) 转换为 KPW3 格式 (1072x1448) 灰度图片
"""

import os
import sys
import subprocess
from pathlib import Path

class ScreensaverConverter:
    def __init__(self):
        self.input_dir = Path("screensavers")
        self.output_dir = Path("kpw3/screensavers")
        self.kpw3_size = (1072, 1448)
        
    def print_header(self):
        """打印转换标题"""
        print("🖼️  Kindle Paperwhite 屏保转换工具")
        print("=" * 40)
        print(f"转换格式：KPW1 → KPW3 ({self.kpw3_size[0]}×{self.kpw3_size[1]})")
        print()
    
    def check_input_directory(self):
        """检查输入目录是否存在并包含PNG文件"""
        if not self.input_dir.exists():
            print(f"❌ 输入目录 '{self.input_dir}' 未找到！")
            return False
        
        png_files = list(self.input_dir.glob("*.png"))
        if not png_files:
            print(f"❌ 在 {self.input_dir} 中未找到PNG文件")
            return False
        
        print(f"📸 找到 {len(png_files)} 个PNG文件待转换")
        return True
    
    def create_output_directory(self):
        """创建输出目录"""
        self.output_dir.mkdir(exist_ok=True)
        print(f"📁 输出目录：{self.output_dir}")
    
    def run_command(self, cmd):
        """安全执行shell命令"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except:
            return False
    
    def check_pil(self):
        """检查PIL/Pillow是否可用"""
        try:
            from PIL import Image
            return True
        except ImportError:
            return False
    
    def check_imagemagick(self):
        """检查ImageMagick是否可用"""
        return self.run_command("convert -version")
    
    def convert_with_pil(self, input_file, output_file):
        """使用PIL转换图片"""
        try:
            from PIL import Image
            with Image.open(input_file) as img:
                # 转为灰度
                if img.mode != 'L':
                    img = img.convert('L')
                # 调整尺寸
                img_resized = img.resize(self.kpw3_size, Image.Resampling.LANCZOS)
                # 保存
                img_resized.save(output_file, 'PNG', optimize=True)
                return True
        except:
            return False
    
    def convert_with_imagemagick(self, input_file, output_file):
        """使用ImageMagick转换图片"""
        cmd = f'convert "{input_file}" -colorspace Gray -resize {self.kpw3_size[0]}x{self.kpw3_size[1]}! "{output_file}"'
        return self.run_command(cmd)
    
    def detect_conversion_method(self):
        """检测可用的转换方法"""
        if self.check_pil():
            print("✅ Python PIL/Pillow 可用")
            return "pil"
        elif self.check_imagemagick():
            print("✅ ImageMagick 可用")
            return "imagemagick"
        else:
            print("❌ 未找到可用的图片处理工具")
            print("请安装：pip install Pillow 或 brew install imagemagick")
            return None
    
    def convert_image(self, input_file, output_file, method):
        """转换单张图片"""
        if method == "pil":
            return self.convert_with_pil(input_file, output_file)
        elif method == "imagemagick":
            return self.convert_with_imagemagick(input_file, output_file)
        return False
    
    def convert_all(self):
        """主转换函数"""
        self.print_header()
        
        # 检查先决条件
        if not self.check_input_directory():
            return False
        
        self.create_output_directory()
        
        # 检测转换方法
        method = self.detect_conversion_method()
        if not method:
            return False
        
        print()
        
        # 获取所有PNG文件
        png_files = sorted(self.input_dir.glob("*.png"))
        
        # 转换每张图片
        success_count = 0
        for png_file in png_files:
            output_file = self.output_dir / png_file.name
            
            print(f"转换中: {png_file.name}", end=" ... ")
            
            if self.convert_image(png_file, output_file, method):
                print("✅")
                success_count += 1
            else:
                print("❌")
        
        # 打印总结
        print()
        print(f"🎉 转换完成！成功转换 {success_count}/{len(png_files)} 张图片")
        
        if success_count > 0:
            print(f"📁 KPW3 屏保已保存到：{self.output_dir}")
            print("💡 运行 'python3 meta-data-generator.py kpw3' 生成元数据文件")
        
        return success_count > 0

def main():
    """主入口"""
    converter = ScreensaverConverter()
    success = converter.convert_all()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
