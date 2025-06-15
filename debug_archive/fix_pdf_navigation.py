#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复PDF目录跳转问题的脚本

主要问题:
1. 目录链接的锚点ID与实际内容的ID不匹配
2. PDF书签的页码计算不准确
3. HTML中的章节ID生成逻辑与目录链接不一致

解决方案:
1. 统一ID生成逻辑
2. 改进页码计算方法
3. 确保目录链接与内容锚点一致
"""

import os
import re
from bs4 import BeautifulSoup

def fix_pdf_navigation_in_epub_to_markdown():
    """
    修复epub_to_markdown.py中的PDF导航问题
    """
    
    # 读取原文件
    script_path = os.path.join(os.path.dirname(__file__), 'epub_to_markdown.py')
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复1: 统一ID生成逻辑
    # 在目录生成部分，确保使用与内容相同的ID生成方式
    old_toc_generation = '''        # Generate table of contents data first
        toc_entries = []
        for item in item_documents_for_pdf:
            try:
                content_str = item.get_content().decode('utf-8', 'ignore')
                soup = BeautifulSoup(content_str, 'html.parser')
                
                # Find chapter title
                title_tag = soup.find(['h1', 'h2', 'h3', 'title'])
                if title_tag:
                    title_text = title_tag.get_text().strip()
                    if title_text:
                        item_id = "item_pdf_" + re.sub(r'[^a-zA-Z0-9_-]', '_', item.get_name())
                        if not (item_id and (item_id[0].isalpha() or item_id[0] == '_')):
                            item_id = "_" + item_id
                        toc_entries.append({'title': title_text, 'id': item_id})
            except:
                pass'''
    
    new_toc_generation = '''        # Generate table of contents data first
        toc_entries = []
        for item in item_documents_for_pdf:
            try:
                content_str = item.get_content().decode('utf-8', 'ignore')
                soup = BeautifulSoup(content_str, 'html.parser')
                
                # Find chapter title (prioritize h1, then h2, h3)
                title_tag = soup.find('h1') or soup.find('h2') or soup.find('h3') or soup.find('title')
                if title_tag:
                    title_text = title_tag.get_text().strip()
                    if title_text and not title_text.startswith('目录'):
                        # 使用与后续内容处理相同的ID生成逻辑
                        item_id = "item_pdf_" + re.sub(r'[^a-zA-Z0-9_-]', '_', item.get_name())
                        if not (item_id and (item_id[0].isalpha() or item_id[0] == '_')):
                            item_id = "_" + item_id
                        toc_entries.append({
                            'title': title_text, 
                            'id': item_id,
                            'item_name': item.get_name()  # 保存原始文件名用于调试
                        })
            except Exception as e:
                print(f"Warning: Could not process item {item.get_name()} for TOC: {e}")
                pass'''
    
    content = content.replace(old_toc_generation, new_toc_generation)
    
    # 修复2: 改进书签页码计算
    old_bookmark_logic = '''                # Extract chapter information for bookmarks
                bookmarks_data = []
                with open(temp_html_filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Find all chapter headings and their IDs, prioritizing h1 tags
                    page_counter = 1
                    for heading in soup.find_all(['h1', 'h2', 'h3']):
                        title = heading.get_text().strip()
                        if title and len(title) > 0 and not title.startswith('目录'):
                            # Skip the table of contents title itself
                            bookmarks_data.append({
                                'title': title[:100],  # Limit title length
                                'page': page_counter,  # Approximate page number
                                'id': heading.get('id', f'heading_{page_counter}')
                            })
                            # Increment page counter for h1 tags (main chapters)
                            if heading.name == 'h1':
                                page_counter += 1'''
    
    new_bookmark_logic = '''                # Extract chapter information for bookmarks
                bookmarks_data = []
                with open(temp_html_filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Find all chapter containers (div.epub-item-content) for more accurate positioning
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
                                        'page': i + 2,  # 从第2页开始（第1页是目录）
                                        'id': chapter_id,
                                        'element_id': heading.get('id', chapter_id)  # 保存元素ID用于调试
                                    })
                                    print(f"Bookmark created: {title[:50]} -> Page {i + 2} (ID: {chapter_id})")
                    
                    # 如果没有找到章节容器，回退到原来的方法
                    if not bookmarks_data:
                        print("Warning: No chapter containers found, using fallback method")
                        page_counter = 2  # 从第2页开始（第1页是目录）
                        for heading in soup.find_all(['h1', 'h2', 'h3']):
                            title = heading.get_text().strip()
                            if title and len(title) > 0 and not title.startswith('目录'):
                                heading_id = heading.get('id', f'heading_{page_counter}')
                                bookmarks_data.append({
                                    'title': title[:100],
                                    'page': page_counter,
                                    'id': heading_id
                                })
                                # 只有h1标签才增加页码（主要章节）
                                if heading.name == 'h1':
                                    page_counter += 1'''
    
    content = content.replace(old_bookmark_logic, new_bookmark_logic)
    
    # 修复3: 改进目录HTML生成，添加调试信息
    old_toc_html = '''            toc_html = """
            <div class="table-of-contents" style="page-break-after: always; margin-bottom: 30px;">
                <h1 style="text-align: center; margin-bottom: 30px; font-family: 'PingFang SC', 'SimHei', 'STHeiti', 'Microsoft YaHei', sans-serif;">目录</h1>
                <div class="toc-list">
            """
            for i, entry in enumerate(toc_entries):
                toc_html += f'<div class="toc-entry"><a href="#{entry["id"]}" style="text-decoration: none; color: #333; display: block; padding: 8px 0; border-bottom: 1px dotted #ccc; font-family: \'PingFang SC\', \'SimHei\', \'STHeiti\', \'Microsoft YaHei\', sans-serif;">{i+1}. {entry["title"]}</a></div>\n'
            toc_html += "</div></div>"'''
    
    new_toc_html = '''            toc_html = """
            <div class="table-of-contents" style="page-break-after: always; margin-bottom: 30px;">
                <h1 style="text-align: center; margin-bottom: 30px; font-family: 'PingFang SC', 'SimHei', 'STHeiti', 'Microsoft YaHei', sans-serif;">目录</h1>
                <div class="toc-list">
            """
            for i, entry in enumerate(toc_entries):
                # 添加调试信息到HTML注释中
                toc_html += f'<!-- TOC Entry {i+1}: {entry["title"]} -> #{entry["id"]} -->\n'
                toc_html += f'<div class="toc-entry"><a href="#{entry["id"]}" style="text-decoration: none; color: #333; display: block; padding: 8px 0; border-bottom: 1px dotted #ccc; font-family: \'PingFang SC\', \'SimHei\', \'STHeiti\', \'Microsoft YaHei\', sans-serif;" title="跳转到: {entry["id"]}">{i+1}. {entry["title"]}</a></div>\n'
                print(f"TOC Entry {i+1}: {entry['title'][:50]} -> #{entry['id']}")
            toc_html += "</div></div>"'''
    
    content = content.replace(old_toc_html, new_toc_html)
    
    # 写入修复后的文件
    backup_path = script_path + '.backup'
    if not os.path.exists(backup_path):
        # 创建备份
        with open(backup_path, 'w', encoding='utf-8') as f:
            with open(script_path, 'r', encoding='utf-8') as original:
                f.write(original.read())
        print(f"Backup created: {backup_path}")
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("PDF navigation fixes applied to epub_to_markdown.py")
    print("\nChanges made:")
    print("1. 统一了目录和内容的ID生成逻辑")
    print("2. 改进了PDF书签的页码计算方法")
    print("3. 添加了调试信息以便排查问题")
    print("4. 优化了章节定位机制")
    
def restore_backup():
    """
    恢复备份文件
    """
    script_path = os.path.join(os.path.dirname(__file__), 'epub_to_markdown.py')
    backup_path = script_path + '.backup'
    
    if os.path.exists(backup_path):
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        
        print(f"Restored from backup: {backup_path}")
    else:
        print("No backup file found")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_backup()
    else:
        fix_pdf_navigation_in_epub_to_markdown()
        print("\n使用方法:")
        print("python fix_pdf_navigation.py          # 应用修复")
        print("python fix_pdf_navigation.py restore  # 恢复备份")