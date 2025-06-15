#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析PDF页面内容和章节分布
"""

import os
from PyPDF2 import PdfReader

def analyze_pdf_pages():
    """
    详细分析PDF每一页的内容
    """
    pdf_file = "test_final/测试书籍/测试书籍.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"错误: PDF文件不存在: {pdf_file}")
        return
    
    print("=" * 60)
    print("PDF页面内容详细分析")
    print("=" * 60)
    
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    print(f"PDF总页数: {total_pages}")
    
    chapters = ["第一章：开始", "第二章：发展", "第三章：结束"]
    chapter_pages = {}
    
    print("\n=== 逐页内容分析 ===")
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        text = page.extract_text()
        
        print(f"\n第{page_num}页:")
        print("-" * 40)
        
        # 显示页面的前500个字符
        preview = text[:500] if text else "(空页面)"
        print(preview)
        
        # 检查章节标题
        found_chapters = []
        for chapter in chapters:
            if chapter in text:
                found_chapters.append(chapter)
                if chapter not in chapter_pages:
                    chapter_pages[chapter] = page_num
        
        if found_chapters:
            print(f"\n  ✓ 发现章节: {', '.join(found_chapters)}")
        
        print("\n" + "=" * 60)
    
    print("\n=== 章节页面分布总结 ===")
    for chapter in chapters:
        if chapter in chapter_pages:
            print(f"{chapter}: 第{chapter_pages[chapter]}页")
        else:
            print(f"{chapter}: 未找到")
    
    # 分析书签
    print("\n=== 书签分析 ===")
    if reader.outline:
        for i, bookmark in enumerate(reader.outline):
            if hasattr(bookmark, 'title'):
                title = bookmark.title
                print(f"书签 {i+1}: {title}")
                
                # 尝试确定书签指向的页面
                if hasattr(bookmark, 'page'):
                    page_ref = bookmark.page
                    print(f"  页面引用: {page_ref}")
                    
                    # 尝试找到对应的页面索引
                    for j, page in enumerate(reader.pages):
                        if page.indirect_reference == page_ref:
                            actual_page = j + 1
                            print(f"  -> 实际指向第{actual_page}页")
                            
                            # 检查该页面是否包含对应章节
                            page_text = page.extract_text()
                            if title in page_text:
                                print(f"  ✓ 页面内容匹配")
                            else:
                                print(f"  ✗ 页面内容不匹配")
                                # 查找该章节实际在哪一页
                                if title in chapter_pages:
                                    expected_page = chapter_pages[title]
                                    offset = actual_page - expected_page
                                    print(f"  应该在第{expected_page}页，偏移量: {offset}")
                            break
                    else:
                        print(f"  -> 无法确定目标页面")
    else:
        print("PDF中没有书签")

if __name__ == "__main__":
    analyze_pdf_pages()