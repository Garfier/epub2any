#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试PDF目录生成的脚本
保留临时HTML文件以便检查目录内容
"""

import os
import sys
from epub_to_markdown import epub_to_markdown

def debug_pdf_generation(epub_file, output_dir):
    """
    调试PDF生成，保留临时文件
    """
    print("开始调试PDF目录生成...")
    
    # 临时修改epub_to_markdown.py以保留HTML文件
    # 我们将直接调用函数并手动检查
    
    if not os.path.exists(epub_file):
        print(f"错误: EPUB文件不存在: {epub_file}")
        return
    
    # 调用转换函数
    epub_to_markdown(epub_file, output_dir, output_format='pdf')
    
    # 查找生成的PDF文件
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"\n生成的PDF文件: {pdf_path}")
                
                # 检查PDF文件大小
                size = os.path.getsize(pdf_path)
                print(f"PDF文件大小: {size} 字节")
                
                # 尝试使用PyPDF2检查PDF内容
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(pdf_path)
                    print(f"PDF页数: {len(reader.pages)}")
                    
                    # 检查书签
                    if reader.outline:
                        print(f"PDF书签数量: {len(reader.outline)}")
                        print("书签列表:")
                        for i, bookmark in enumerate(reader.outline):
                            if hasattr(bookmark, 'title'):
                                print(f"  {i+1}. {bookmark.title}")
                            else:
                                print(f"  {i+1}. {bookmark}")
                    else:
                        print("PDF中没有找到书签")
                        
                    # 检查第一页内容
                    if len(reader.pages) > 0:
                        first_page = reader.pages[0]
                        text = first_page.extract_text()
                        print(f"\n第一页文本内容（前500字符）:")
                        print(text[:500])
                        
                        # 检查是否包含"目录"字样（包括各种编码形式）
                        if "目录" in text or "⽬录" in text or "目" in text:
                            print("✓ 第一页包含目录相关字样")
                        else:
                            print("✗ 第一页不包含目录相关字样")
                            
                        # 检查是否包含章节标题
                        chapter_found = False
                        for chapter in ["第一章", "第二章", "第三章", "第⼀章", "第⼆章"]:
                            if chapter in text:
                                chapter_found = True
                                break
                        if chapter_found:
                            print("✓ 第一页包含章节标题")
                        else:
                            print("✗ 第一页不包含章节标题")
                            
                except Exception as e:
                    print(f"检查PDF内容时出错: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("使用方法: python debug_pdf_toc.py <epub_file> <output_dir>")
        sys.exit(1)
    
    epub_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    debug_pdf_generation(epub_file, output_dir)