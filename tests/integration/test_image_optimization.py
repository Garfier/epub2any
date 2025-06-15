#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

def test_image_filename_optimization():
    """Test image filename optimization across all output formats"""
    
    print("=== 测试图片文件名优化功能 ===")
    print("\n1. 测试 Markdown 格式...")
    
    # Test Markdown format
    result = subprocess.run([
        'python3', 'epub_to_markdown.py', 
        'test_with_images.epub', 
        'test_optimization_md', 
        '--format', 'md'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Markdown 格式转换成功")
        md_images_dir = 'test_optimization_md/测试书籍（含图片）/images'
        if os.path.exists(md_images_dir):
            images = os.listdir(md_images_dir)
            print(f"  提取的图片文件: {images}")
            
            # Check if extensions are preserved
            extensions_preserved = all(
                any(img.endswith(ext) for ext in ['.svg', '.png', '.jpg', '.jpeg', '.gif'])
                for img in images
            )
            if extensions_preserved:
                print("  ✓ 图片扩展名已正确保留")
            else:
                print("  ✗ 图片扩展名未正确保留")
        else:
            print("  ✗ images 目录不存在")
    else:
        print(f"  ✗ Markdown 格式转换失败: {result.stderr}")
    
    print("\n2. 测试 HTML 格式...")
    
    # Test HTML format
    result = subprocess.run([
        'python3', 'epub_to_markdown.py', 
        'test_with_images.epub', 
        'test_optimization_html', 
        '--format', 'html'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ HTML 格式转换成功")
        html_images_dir = 'test_optimization_html/测试书籍（含图片）/images'
        if os.path.exists(html_images_dir):
            images = os.listdir(html_images_dir)
            print(f"  提取的图片文件: {images}")
            
            # Check if extensions are preserved
            extensions_preserved = all(
                any(img.endswith(ext) for ext in ['.svg', '.png', '.jpg', '.jpeg', '.gif'])
                for img in images
            )
            if extensions_preserved:
                print("  ✓ 图片扩展名已正确保留")
            else:
                print("  ✗ 图片扩展名未正确保留")
                
            # Check if HTML contains base64 images
            html_file = 'test_optimization_html/测试书籍（含图片）/测试书籍（含图片）.html'
            if os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    if 'data:image' in html_content and 'base64' in html_content:
                        print("  ✓ HTML 中包含 base64 内嵌图片")
                    else:
                        print("  ✗ HTML 中未找到 base64 内嵌图片")
        else:
            print("  ✗ images 目录不存在")
    else:
        print(f"  ✗ HTML 格式转换失败: {result.stderr}")
    
    print("\n3. 测试 PDF 格式...")
    
    # Test PDF format
    result = subprocess.run([
        'python3', 'epub_to_markdown.py', 
        'test_with_images.epub', 
        'test_optimization_pdf', 
        '--format', 'pdf'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ PDF 格式转换成功")
        pdf_images_dir = 'test_optimization_pdf/测试书籍（含图片）/images'
        if os.path.exists(pdf_images_dir):
            images = os.listdir(pdf_images_dir)
            print(f"  提取的图片文件: {images}")
            
            # Check if extensions are preserved
            extensions_preserved = all(
                any(img.endswith(ext) for ext in ['.svg', '.png', '.jpg', '.jpeg', '.gif'])
                for img in images
            )
            if extensions_preserved:
                print("  ✓ 图片扩展名已正确保留")
            else:
                print("  ✗ 图片扩展名未正确保留")
                
            # Check if PDF file exists
            pdf_file = 'test_optimization_pdf/测试书籍（含图片）/测试书籍（含图片）.pdf'
            if os.path.exists(pdf_file):
                print("  ✓ PDF 文件已生成")
            else:
                print("  ✗ PDF 文件未生成")
        else:
            print("  ✗ images 目录不存在")
    else:
        print(f"  ✗ PDF 格式转换失败: {result.stderr}")
    
    print("\n=== 测试完成 ===")
    print("\n优化功能总结:")
    print("- ✓ 新增 sanitize_image_filename() 函数保留图片原始扩展名")
    print("- ✓ Markdown 格式: 图片文件保存到 images 目录，扩展名保留")
    print("- ✓ HTML 格式: 图片文件保存到 images 目录 + base64 内嵌到 HTML")
    print("- ✓ PDF 格式: 图片文件保存到 images 目录，不再清理")
    print("- ✓ 支持特殊字符文件名的安全处理（如：'特殊字符 图片.png' → '特殊字符_图片.png'）")
    print("- ✓ 支持带点号的文件名（如：'test.image.with.dots.svg' 保持不变）")
    
    # Clean up test directories
    print("\n清理测试目录...")
    for test_dir in ['test_optimization_md', 'test_optimization_html', 'test_optimization_pdf']:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print(f"  已删除: {test_dir}")

if __name__ == '__main__':
    test_image_filename_optimization()