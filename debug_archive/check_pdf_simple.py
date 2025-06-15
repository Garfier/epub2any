#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的PDF检查脚本
"""

import os

def check_pdf_simple():
    pdf_file = "test_final/测试书籍/测试书籍.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"PDF文件不存在: {pdf_file}")
        return
    
    print(f"检查PDF文件: {pdf_file}")
    print(f"文件大小: {os.path.getsize(pdf_file)} 字节")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_file)
        print(f"PDF页数: {len(reader.pages)}")
        
        # 检查书签
        if reader.outline:
            print(f"书签数量: {len(reader.outline)}")
            print("书签列表:")
            for i, bookmark in enumerate(reader.outline):
                if hasattr(bookmark, 'title'):
                    print(f"  {i+1}. {bookmark.title}")
                else:
                    print(f"  {i+1}. {bookmark}")
        else:
            print("没有找到书签")
        
        # 检查第一页内容
        if len(reader.pages) > 0:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            print(f"\n第一页文本内容（前500字符）:")
            print("-" * 40)
            print(text[:500])
            print("-" * 40)
            
            # 检查是否包含目录
            if "目录" in text:
                print("✓ 第一页包含目录")
            else:
                print("✗ 第一页不包含目录")
            
            # 检查章节
            chapters = ["第一章", "第二章", "第三章"]
            found_chapters = []
            for chapter in chapters:
                if chapter in text:
                    found_chapters.append(chapter)
            
            if found_chapters:
                print(f"✓ 第一页找到章节: {', '.join(found_chapters)}")
            else:
                print("✗ 第一页没有找到章节标题")
                
    except ImportError:
        print("需要安装PyPDF2: pip install PyPDF2")
    except Exception as e:
        print(f"检查PDF时出错: {e}")

if __name__ == '__main__':
    check_pdf_simple()