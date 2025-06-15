#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试PDF链接跳转位置的脚本
"""

import os
import re
from bs4 import BeautifulSoup
from epub_to_markdown import epub_to_markdown

def debug_pdf_links():
    """
    调试PDF链接和跳转位置
    """
    print("=" * 60)
    print("调试PDF链接跳转位置")
    print("=" * 60)
    
    # 重新生成PDF并保留临时HTML文件
    epub_file = "test.epub"
    output_dir = "debug_links"
    
    if not os.path.exists(epub_file):
        print(f"错误: 测试EPUB文件不存在: {epub_file}")
        return False
    
    # 清理之前的输出
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    
    print(f"正在生成PDF用于调试: {epub_file} -> {output_dir}")
    
    try:
        # 生成PDF
        epub_to_markdown(epub_file, output_dir, output_format='pdf')
        
        # 查找生成的PDF文件和临时HTML文件
        pdf_files = []
        html_files = []
        
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
                elif file.endswith('.html') and '_temp_' in file:
                    html_files.append(os.path.join(root, file))
        
        if not pdf_files:
            print("错误: 没有找到生成的PDF文件")
            return False
        
        pdf_file = pdf_files[0]
        print(f"\n找到PDF文件: {pdf_file}")
        
        # 分析HTML结构
        if html_files:
            html_file = html_files[0]
            print(f"找到临时HTML文件: {html_file}")
            analyze_html_structure(html_file)
        else:
            print("警告: 没有找到临时HTML文件")
        
        # 分析PDF书签
        analyze_pdf_bookmarks(pdf_file)
        
        return True
        
    except Exception as e:
        print(f"错误: 调试过程失败: {e}")
        return False

def analyze_html_structure(html_file):
    """
    分析HTML结构
    """
    print("\n=== HTML结构分析 ===")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 分析目录部分
        print("\n--- 目录部分分析 ---")
        toc_div = soup.find('div', class_='table-of-contents')
        if toc_div:
            print("✓ 找到目录容器")
            
            # 检查目录链接
            toc_links = toc_div.find_all('a')
            print(f"目录链接数量: {len(toc_links)}")
            
            for i, link in enumerate(toc_links):
                href = link.get('href', '')
                text = link.get_text().strip()
                title_attr = link.get('title', '')
                print(f"  {i+1}. 文本: '{text}'")
                print(f"      链接: {href}")
                print(f"      标题: {title_attr}")
                
                # 检查对应的锚点是否存在
                if href.startswith('#'):
                    anchor_id = href[1:]
                    target_element = soup.find(id=anchor_id)
                    if target_element:
                        print(f"      ✓ 找到锚点: {anchor_id}")
                        print(f"      锚点标签: {target_element.name}")
                        print(f"      锚点类: {target_element.get('class', [])}")
                        
                        # 检查锚点在文档中的位置
                        position = get_element_position(soup, target_element)
                        print(f"      锚点位置: 第{position}个元素")
                    else:
                        print(f"      ✗ 未找到锚点: {anchor_id}")
                print()
        else:
            print("✗ 未找到目录容器")
        
        # 分析章节容器
        print("\n--- 章节容器分析 ---")
        chapter_divs = soup.find_all('div', class_='epub-item-content')
        print(f"章节容器数量: {len(chapter_divs)}")
        
        for i, div in enumerate(chapter_divs):
            div_id = div.get('id', '未知')
            heading = div.find(['h1', 'h2', 'h3'])
            if heading:
                title = heading.get_text().strip()
                print(f"  {i+1}. ID: {div_id}")
                print(f"      标题: {title}")
                print(f"      标题标签: {heading.name}")
                
                # 检查容器在文档中的位置
                position = get_element_position(soup, div)
                print(f"      容器位置: 第{position}个元素")
                
                # 检查容器内容长度
                content_length = len(div.get_text())
                print(f"      内容长度: {content_length}字符")
            else:
                print(f"  {i+1}. ID: {div_id} -> 无标题")
            print()
                
    except Exception as e:
        print(f"分析HTML结构时出错: {e}")

def get_element_position(soup, target_element):
    """
    获取元素在文档中的位置
    """
    all_elements = soup.find_all()
    for i, element in enumerate(all_elements):
        if element == target_element:
            return i + 1
    return -1

def analyze_pdf_bookmarks(pdf_file):
    """
    分析PDF书签
    """
    print("\n=== PDF书签分析 ===")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(pdf_file)
        print(f"PDF总页数: {len(reader.pages)}")
        
        # 检查书签
        if reader.outline:
            print(f"\n书签数量: {len(reader.outline)}")
            print("书签详细信息:")
            
            for i, bookmark in enumerate(reader.outline):
                if hasattr(bookmark, 'title'):
                    title = bookmark.title
                    print(f"  {i+1}. 标题: {title}")
                    
                    # 尝试获取页码信息
                    try:
                        if hasattr(bookmark, 'page'):
                            page_info = bookmark.page
                            if hasattr(page_info, 'idnum'):
                                page_num = None
                                # 尝试找到页码
                                for page_idx, page in enumerate(reader.pages):
                                    if page.idnum == page_info.idnum:
                                        page_num = page_idx + 1
                                        break
                                
                                if page_num:
                                    print(f"      指向页面: 第{page_num}页")
                                else:
                                    print(f"      页面ID: {page_info.idnum} (无法确定页码)")
                            else:
                                print(f"      页面对象: {page_info}")
                        else:
                            print(f"      无页面信息")
                    except Exception as e:
                        print(f"      获取页面信息失败: {e}")
                else:
                    print(f"  {i+1}. {bookmark}")
                print()
        else:
            print("\n没有找到书签")
        
        # 分析每页内容
        print("\n--- 各页内容分析 ---")
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            print(f"第{page_num}页:")
            print(f"  文本行数: {len(lines)}")
            if lines:
                print(f"  首行: {lines[0][:50]}...")
                if len(lines) > 1:
                    print(f"  末行: {lines[-1][:50]}...")
            
            # 检查是否包含章节标题
            chapter_titles = ["第一章", "第二章", "第三章"]
            found_titles = []
            for title in chapter_titles:
                if title in text:
                    found_titles.append(title)
            
            if found_titles:
                print(f"  包含章节: {', '.join(found_titles)}")
            print()
                
    except ImportError:
        print("需要安装PyPDF2: pip install PyPDF2")
    except Exception as e:
        print(f"分析PDF书签时出错: {e}")

def main():
    success = debug_pdf_links()
    
    if success:
        print("\n=== 调试完成 ===")
        print("请检查上述分析结果，重点关注:")
        print("1. 目录链接的href是否正确指向章节ID")
        print("2. 章节容器的ID是否与目录链接匹配")
        print("3. PDF书签是否指向正确的页面")
        print("4. 各页内容分布是否合理")
    else:
        print("\n=== 调试失败 ===")

if __name__ == '__main__':
    main()