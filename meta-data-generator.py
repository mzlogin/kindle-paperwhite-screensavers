import hashlib
import os
import json
import sys

def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
        return str(_hash).lower()

def generate_meta_data(screensavers_path, output_file):
    """为指定目录生成元数据文件"""
    if not os.path.exists(screensavers_path):
        print(f"❌ 目录 '{screensavers_path}' 不存在！")
        return False
    
    file_md5_dict = {}
    png_count = 0
    
    for dir_path, dir_names, filenames in os.walk(screensavers_path):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.png':
                file_path = os.path.join(screensavers_path, filename)
                try:
                    file_md5_dict[filename] = get_file_md5(file_path)
                    png_count += 1
                    print(f"✅ {filename}")
                except Exception as e:
                    print(f"❌ 处理 {filename} 时出错: {e}")
    
    if png_count == 0:
        print(f"❌ 在 {screensavers_path} 中未找到PNG文件")
        return False
    
    try:
        with open(output_file, 'w') as outfile:
            json.dump(file_md5_dict, outfile, indent=2)
        
        print(f"\n🎉 元数据生成成功！")
        print(f"📁 输出文件：{output_file}")
        print(f"📸 处理了 {png_count} 个PNG文件")
        return True
    except Exception as e:
        print(f"❌ 写入 {output_file} 时出错: {e}")
        return False

if __name__ == '__main__':
    print("📋 Kindle 屏保元数据生成器")
    print("=" * 30)
    
    # 默认为原始目录生成
    screensavers_path = 'screensavers'
    output_file = 'meta.json'
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == 'kpw3':
            screensavers_path = 'kpw3/screensavers'
            output_file = 'kpw3/meta.json'
            print("🎯 为 KPW3 屏保生成元数据")
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("用法:")
            print("  python3 meta-data-generator.py        # 为原始屏保生成 meta.json")
            print("  python3 meta-data-generator.py kpw3   # 为KPW3屏保生成 meta_kpw3.json")
            sys.exit(0)
    else:
        print("🎯 为原始屏保生成元数据")
    
    print()
    success = generate_meta_data(screensavers_path, output_file)
    
    sys.exit(0 if success else 1)
