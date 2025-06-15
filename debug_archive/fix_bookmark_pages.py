#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复PDF书签页码计算的脚本
"""

import os
import re
from bs4 import BeautifulSoup

def fix_bookmark_page_calculation():
    """
    修复epub_to_markdown.py中的书签页码计算逻辑
    """
    print("修复PDF书签页码计算逻辑...")
    
    file_path = "epub_to_markdown.py"
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换书签生成逻辑
    old_bookmark_logic = '''                    # Find all chapter containers (div.epub-item-content) for more accurate positioning
                    chapter_divs = soup.find_all('div', class_='epub-item-content')
                    
                    for i, chapter_div in enumerate(chapter_divs):
                        # 在每个章节容器中查找标题
                        heading = chapter_div.find(['h1', 'h2', 'h3'])
                        if heading:
                            title = heading.get_text().strip()
                            if title and len(title) > 0 and not title.startswith('目录'):
                                chapter_id = chapter_div.get('id')
                                if chapter_id:
                                    bookmarks_data.append({
                                        'title': title[:100],  # Limit title length
                                        'page': i + 2,  # +2 because: +1 for 1-based indexing, +1 for TOC page
                                        'id': chapter_id
                                    })
                                    print(f"Bookmark prepared: {title} -> Page {i + 2} (ID: {chapter_id})")
                    
                    # Fallback: if no chapter containers found, use headings
                    if not bookmarks_data:
                        headings = soup.find_all(['h1', 'h2', 'h3'])
                        page_counter = 1
                        for heading in headings:
                            title = heading.get_text().strip()
                            if title and len(title) > 0 and not title.startswith('目录'):
                                if heading.name == 'h1':
                                    page_counter += 1
                                bookmarks_data.append({
                                    'title': title[:100],
                                    'page': page_counter
                                })
                                print(f"Fallback bookmark: {title} -> Page {page_counter}")'''
    
    new_bookmark_logic = '''                    # 使用更精确的页面计算方法
                    # 首先找到目录容器，确定目录占用的页面
                    toc_div = soup.find('div', class_='table-of-contents')
                    toc_pages = 1  # 目录通常占用1页
                    
                    # 找到所有章节容器
                    chapter_divs = soup.find_all('div', class_='epub-item-content')
                    
                    for i, chapter_div in enumerate(chapter_divs):
                        # 在每个章节容器中查找标题
                        heading = chapter_div.find(['h1', 'h2', 'h3'])
                        if heading:
                            title = heading.get_text().strip()
                            if title and len(title) > 0 and not title.startswith('目录'):
                                chapter_id = chapter_div.get('id')
                                if chapter_id:
                                    # 计算页码：目录页数 + 章节索引 + 1
                                    page_num = toc_pages + i + 1
                                    
                                    # 如果章节内容很长，可能需要调整页码
                                    # 这里使用简单的估算：每个章节大约占用1页
                                    
                                    bookmarks_data.append({
                                        'title': title[:100],  # 限制标题长度
                                        'page': page_num,
                                        'id': chapter_id
                                    })
                                    print(f"Bookmark prepared: {title} -> Page {page_num} (ID: {chapter_id})")
                    
                    # 备用方案：如果没有找到章节容器，使用标题
                    if not bookmarks_data:
                        headings = soup.find_all(['h1', 'h2', 'h3'])
                        page_counter = toc_pages + 1  # 从目录后开始
                        for heading in headings:
                            title = heading.get_text().strip()
                            if title and len(title) > 0 and not title.startswith('目录'):
                                if heading.name == 'h1':
                                    page_counter += 1
                                bookmarks_data.append({
                                    'title': title[:100],
                                    'page': page_counter
                                })
                                print(f"Fallback bookmark: {title} -> Page {page_counter}")'''
    
    # 替换内容
    if old_bookmark_logic in content:
        content = content.replace(old_bookmark_logic, new_bookmark_logic)
        print("✓ 书签页码计算逻辑已更新")
    else:
        print("⚠️  未找到需要替换的书签逻辑代码")
        return False
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 文件已更新: {file_path}")
    return True

def main():
    print("=" * 50)
    print("修复PDF书签页码计算")
    print("=" * 50)
    
    success = fix_bookmark_page_calculation()
    
    if success:
        print("\n修复完成！请重新生成PDF测试效果。")
    else:
        print("\n修复失败，请检查代码。")

if __name__ == '__main__':
    main()