#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF导航修复效果的脚本

这个脚本会:
1. 生成测试PDF
2. 检查PDF书签
3. 验证目录链接
4. 分析可能的问题
"""

import os
import sys
from epub_to_markdown import epub_to_markdown

def test_pdf_navigation_fix():
    """
    测试PDF导航修复效果
    """
    print("=" * 60)
    print("测试PDF导航修复效果")
    print("=" * 60)
    
    # 使用测试EPUB文件
    epub_file = "test.epub"
    output_dir = "test_navigation_fix"
    
    if not os.path.exists(epub_file):
        print(f"错误: 测试EPUB文件不存在: {epub_file}")
        return False
    
    # 清理之前的输出
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    
    print(f"正在生成PDF: {epub_file} -> {output_dir}")
    print("\n--- PDF生成过程 ---")
    
    try:
        # 生成PDF
        epub_to_markdown(epub_file, output_dir, output_format='pdf')
        
        print("\n--- PDF生成完成 ---")
        
        # 查找生成的PDF文件
        pdf_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        if not pdf_files:
            print("错误: 没有找到生成的PDF文件")
            return False
        
        pdf_file = pdf_files[0]
        print(f"\n找到PDF文件: {pdf_file}")
        
        # 分析PDF内容
        analyze_pdf_content(pdf_file)
        
        # 检查临时HTML文件（如果存在）
        check_temp_html(output_dir)
        
        return True
        
    except Exception as e:
        print(f"错误: PDF生成失败: {e}")
        return False

def analyze_pdf_content(pdf_file):
    """
    分析PDF内容和书签
    """
    print("\n=== PDF内容分析 ===")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_file)
        print(f"PDF页数: {len(reader.pages)}")
        
        # 检查书签
        if reader.outline:
            print(f"\n书签数量: {len(reader.outline)}")
            print("书签列表:")
            for i, bookmark in enumerate(reader.outline):
                if hasattr(bookmark, 'title'):
                    print(f"  {i+1}. {bookmark.title}")
                    # 尝试获取页码信息
                    try:
                        if hasattr(bookmark, 'page'):
                            page_info = bookmark.page
                            if hasattr(page_info, 'idnum'):
                                print(f"      -> 页面ID: {page_info.idnum}")
                    except:
                        pass
                else:
                    print(f"  {i+1}. {bookmark}")
        else:
            print("\n⚠️  PDF中没有找到书签")
        
        # 检查第一页内容（目录页）
        if len(reader.pages) > 0:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            print(f"\n第一页文本内容（前800字符）:")
            print("-" * 40)
            print(text[:800])
            print("-" * 40)
            
            # 检查目录相关内容
            if "目录" in text:
                print("✓ 第一页包含目录")
            else:
                print("✗ 第一页不包含目录")
            
            # 检查章节标题
            chapters = ["第一章", "第二章", "第三章"]
            found_chapters = []
            for chapter in chapters:
                if chapter in text:
                    found_chapters.append(chapter)
            
            if found_chapters:
                print(f"✓ 找到章节: {', '.join(found_chapters)}")
            else:
                print("✗ 没有找到章节标题")
                
    except ImportError:
        print("需要安装PyPDF2: pip install PyPDF2")
    except Exception as e:
        print(f"分析PDF时出错: {e}")

def check_temp_html(output_dir):
    """
    检查临时HTML文件（如果存在）
    """
    print("\n=== 临时HTML文件检查 ===")
    
    # 查找临时HTML文件
    html_files = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.html') and '_temp_' in file:
                html_files.append(os.path.join(root, file))
    
    if html_files:
        html_file = html_files[0]
        print(f"找到临时HTML文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 检查目录部分
            toc_div = soup.find('div', class_='table-of-contents')
            if toc_div:
                print("✓ 找到目录容器")
                
                # 检查目录链接
                toc_links = toc_div.find_all('a')
                print(f"目录链接数量: {len(toc_links)}")
                
                for i, link in enumerate(toc_links):
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    print(f"  {i+1}. {text} -> {href}")
                    
                    # 检查对应的锚点是否存在
                    if href.startswith('#'):
                        anchor_id = href[1:]
                        target_element = soup.find(id=anchor_id)
                        if target_element:
                            print(f"      ✓ 找到对应锚点: {anchor_id}")
                        else:
                            print(f"      ✗ 未找到对应锚点: {anchor_id}")
            else:
                print("✗ 未找到目录容器")
            
            # 检查章节容器
            chapter_divs = soup.find_all('div', class_='epub-item-content')
            print(f"\n章节容器数量: {len(chapter_divs)}")
            
            for i, div in enumerate(chapter_divs):
                div_id = div.get('id', '未知')
                heading = div.find(['h1', 'h2', 'h3'])
                if heading:
                    title = heading.get_text().strip()
                    print(f"  {i+1}. ID: {div_id} -> 标题: {title}")
                else:
                    print(f"  {i+1}. ID: {div_id} -> 无标题")
                    
        except Exception as e:
            print(f"分析HTML文件时出错: {e}")
    else:
        print("没有找到临时HTML文件（已被清理）")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'analyze':
            # 只分析现有的PDF文件
            pdf_file = "test_navigation_fix/测试书籍/测试书籍.pdf"
            if os.path.exists(pdf_file):
                analyze_pdf_content(pdf_file)
            else:
                print(f"PDF文件不存在: {pdf_file}")
            return
    
    # 完整测试
    success = test_pdf_navigation_fix()
    
    if success:
        print("\n=== 测试完成 ===")
        print("请检查生成的PDF文件，验证:")
        print("1. 目录链接是否可以正确跳转")
        print("2. PDF书签是否指向正确位置")
        print("3. 页码是否准确")
        
        pdf_file = "test_navigation_fix/测试书籍/测试书籍.pdf"
        if os.path.exists(pdf_file):
            print(f"\nPDF文件位置: {os.path.abspath(pdf_file)}")
    else:
        print("\n=== 测试失败 ===")

if __name__ == '__main__':
    main()