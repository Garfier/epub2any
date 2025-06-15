#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF书签修复效果
"""

import os
import sys
from epub_to_markdown import epub_to_markdown

def test_bookmark_fix():
    """
    测试修复后的PDF书签功能
    """
    print("=" * 60)
    print("测试PDF书签修复效果")
    print("=" * 60)
    
    epub_file = "test.epub"
    output_dir = "test_final"
    
    if not os.path.exists(epub_file):
        print(f"错误: EPUB文件不存在: {epub_file}")
        return False
    
    print(f"输入文件: {epub_file}")
    print(f"输出目录: {output_dir}")
    print("\n开始转换...")
    
    try:
        # 调用转换函数
        epub_to_markdown(epub_file, output_dir, output_format='pdf')
        
        # 检查生成的PDF
        pdf_file = os.path.join(output_dir, "测试书籍", "测试书籍.pdf")
        if os.path.exists(pdf_file):
            print(f"\n✓ PDF文件已生成: {pdf_file}")
            
            # 分析PDF内容
            analyze_pdf_bookmarks(pdf_file)
            return True
        else:
            print(f"\n✗ PDF文件未找到: {pdf_file}")
            return False
            
    except Exception as e:
        print(f"\n✗ 转换失败: {e}")
        return False

def analyze_pdf_bookmarks(pdf_file):
    """
    分析PDF书签
    """
    print("\n=== PDF书签分析 ===")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_file)
        print(f"PDF总页数: {len(reader.pages)}")
        print(f"文件大小: {os.path.getsize(pdf_file):,} 字节")
        
        # 检查书签
        if reader.outline:
            print(f"\n书签数量: {len(reader.outline)}")
            print("书签详细信息:")
            
            for i, bookmark in enumerate(reader.outline):
                if hasattr(bookmark, 'title'):
                    title = bookmark.title
                    print(f"  {i+1}. {title}")
                    
                    # 尝试获取页码信息
                    try:
                        if hasattr(bookmark, 'page'):
                            page_info = bookmark.page
                            if hasattr(page_info, 'idnum'):
                                page_num = None
                                for j, page in enumerate(reader.pages):
                                    if page.idnum == page_info.idnum:
                                        page_num = j + 1
                                        break
                                if page_num:
                                    print(f"     -> 指向页面: {page_num}")
                                else:
                                    print(f"     -> 页面ID: {page_info.idnum}")
                            else:
                                print(f"     -> 页面对象: {page_info}")
                    except Exception as e:
                        print(f"     -> 页码信息获取失败: {e}")
        else:
            print("\n⚠️  PDF中没有书签")
        
        # 检查第一页内容
        print("\n=== 第一页内容检查 ===")
        first_page = reader.pages[0]
        first_page_text = first_page.extract_text()
        
        if "目录" in first_page_text:
            print("✓ 第一页包含目录")
        else:
            print("✗ 第一页不包含目录")
        
        # 检查章节标题
        chapters = ["第一章", "第二章", "第三章"]
        for chapter in chapters:
            if chapter in first_page_text:
                print(f"✓ 目录中包含: {chapter}")
            else:
                print(f"✗ 目录中缺少: {chapter}")
                
    except ImportError:
        print("需要安装PyPDF2: pip install PyPDF2")
    except Exception as e:
        print(f"分析PDF时出错: {e}")

def main():
    success = test_bookmark_fix()
    
    if success:
        print("\n✓ 测试完成")
    else:
        print("\n✗ 测试失败")
        sys.exit(1)

if __name__ == '__main__':
    main()