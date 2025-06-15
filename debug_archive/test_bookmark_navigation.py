#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF书签导航功能
"""

import os

def test_pdf_bookmark_navigation():
    """
    测试PDF书签导航功能
    """
    print("=" * 60)
    print("测试PDF书签导航功能")
    print("=" * 60)
    
    pdf_file = "test_final/测试书籍/测试书籍.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"错误: PDF文件不存在: {pdf_file}")
        return False
    
    print(f"分析PDF文件: {pdf_file}")
    print(f"文件大小: {os.path.getsize(pdf_file):,} 字节")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        print(f"PDF总页数: {total_pages}")
        
        # 分析每一页的内容
        print("\n=== 页面内容分析 ===")
        for i, page in enumerate(reader.pages):
            page_num = i + 1
            text = page.extract_text()
            print(f"\n第{page_num}页内容:")
            print("-" * 40)
            # 只显示前200个字符
            preview = text[:200].replace('\n', ' ').strip()
            print(f"{preview}..." if len(text) > 200 else preview)
            
            # 检查是否包含章节标题
            chapters = ["第一章：开始", "第二章：发展", "第三章：结束"]
            for chapter in chapters:
                if chapter in text:
                    print(f"  ✓ 包含章节: {chapter}")
        
        # 分析书签
        print("\n=== 书签分析 ===")
        if reader.outline:
            print(f"书签数量: {len(reader.outline)}")
            
            for i, bookmark in enumerate(reader.outline):
                if hasattr(bookmark, 'title'):
                    title = bookmark.title
                    print(f"\n书签 {i+1}: {title}")
                    
                    # 尝试获取目标页面
                    try:
                        if hasattr(bookmark, 'page'):
                            page_ref = bookmark.page
                            
                            # 查找页面索引
                            target_page = None
                            if hasattr(page_ref, 'idnum'):
                                for j, page in enumerate(reader.pages):
                                    if hasattr(page, 'idnum') and page.idnum == page_ref.idnum:
                                        target_page = j + 1
                                        break
                            
                            if target_page:
                                print(f"  -> 目标页面: {target_page}")
                                
                                # 检查目标页面是否包含相应的章节内容
                                target_page_text = reader.pages[target_page - 1].extract_text()
                                if title in target_page_text:
                                    print(f"  ✓ 页面内容匹配: 第{target_page}页包含'{title}'")
                                else:
                                    print(f"  ✗ 页面内容不匹配: 第{target_page}页不包含'{title}'")
                                    # 显示实际内容
                                    preview = target_page_text[:100].replace('\n', ' ').strip()
                                    print(f"    实际内容: {preview}...")
                            else:
                                print(f"  -> 无法确定目标页面 (页面引用: {page_ref})")
                        else:
                            print(f"  -> 无页面信息")
                    except Exception as e:
                        print(f"  -> 获取页面信息失败: {e}")
        else:
            print("PDF中没有书签")
        
        # 检查目录页
        print("\n=== 目录页检查 ===")
        first_page_text = reader.pages[0].extract_text()
        if "目录" in first_page_text or "⽬录" in first_page_text:
            print("✓ 第一页包含目录")
            
            # 检查目录中的链接
            chapters = ["第一章：开始", "第二章：发展", "第三章：结束"]
            for chapter in chapters:
                if chapter in first_page_text:
                    print(f"  ✓ 目录包含: {chapter}")
                else:
                    print(f"  ✗ 目录缺少: {chapter}")
        else:
            print("✗ 第一页不包含目录")
        
        return True
        
    except ImportError:
        print("需要安装PyPDF2: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"分析PDF时出错: {e}")
        return False

def main():
    success = test_pdf_bookmark_navigation()
    
    if success:
        print("\n=== 测试总结 ===")
        print("✓ PDF书签导航测试完成")
        print("\n建议:")
        print("1. 检查书签是否指向正确的页面")
        print("2. 验证页面内容是否与书签标题匹配")
        print("3. 确认目录页包含所有章节")
    else:
        print("\n✗ 测试失败")

if __name__ == '__main__':
    main()