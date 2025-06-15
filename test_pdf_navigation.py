#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF导航功能的脚本

这个脚本演示了如何使用优化后的epub2any工具生成带有目录和书签导航的PDF文件。

使用方法:
    python test_pdf_navigation.py <epub_file_path> <output_directory>

示例:
    python test_pdf_navigation.py sample.epub output_test
"""

import sys
import os
from epub_to_markdown import epub_to_markdown

def test_pdf_with_navigation(epub_file, output_dir):
    """
    测试PDF生成功能，包括目录和书签导航
    
    Args:
        epub_file (str): EPUB文件路径
        output_dir (str): 输出目录
    """
    print("=" * 60)
    print("测试PDF导航功能")
    print("=" * 60)
    
    if not os.path.exists(epub_file):
        print(f"错误: EPUB文件不存在: {epub_file}")
        return False
    
    if not epub_file.lower().endswith('.epub'):
        print(f"错误: 请提供有效的EPUB文件: {epub_file}")
        return False
    
    try:
        print(f"正在处理EPUB文件: {epub_file}")
        print(f"输出目录: {output_dir}")
        print("\n开始转换...")
        
        # 调用优化后的PDF转换功能
        epub_to_markdown(epub_file, output_dir, output_format='pdf')
        
        print("\n=" * 60)
        print("转换完成!")
        print("=" * 60)
        
        # 检查生成的文件
        if os.path.exists(output_dir):
            print(f"\n生成的文件:")
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if file.endswith('.pdf'):
                        pdf_path = os.path.join(root, file)
                        file_size = os.path.getsize(pdf_path)
                        print(f"  📄 {pdf_path} ({file_size:,} bytes)")
        
        print("\n✨ 新功能特性:")
        print("  • 📖 自动生成目录页面")
        print("  • 🔗 支持章节间跳转链接")
        print("  • 📑 PDF书签导航 (需要PyPDF2)")
        print("  • 📄 页码显示")
        print("  • 🎨 优化的排版和样式")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 转换过程中出现错误: {e}")
        return False

def main():
    """
    主函数
    """
    if len(sys.argv) != 3:
        print("使用方法: python test_pdf_navigation.py <epub_file> <output_directory>")
        print("\n示例:")
        print("  python test_pdf_navigation.py sample.epub output_test")
        sys.exit(1)
    
    epub_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    success = test_pdf_with_navigation(epub_file, output_dir)
    
    if success:
        print("\n🎉 测试成功完成!")
        sys.exit(0)
    else:
        print("\n❌ 测试失败!")
        sys.exit(1)

if __name__ == '__main__':
    main()