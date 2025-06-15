#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epub2any - 统一的EPUB转换工具
支持将EPUB文件转换为多种格式：Markdown、HTML、PDF
同时提供PDF目录生成和调试功能
"""

import argparse
import os
import sys
from epub_to_markdown import epub_to_markdown

def debug_pdf_generation(epub_file, output_dir):
    """
    调试PDF生成，保留临时文件并检查PDF内容
    """
    print("开始调试PDF目录生成...")
    
    if not os.path.exists(epub_file):
        print(f"错误: EPUB文件不存在: {epub_file}")
        return False
    
    # 调用转换函数
    epub_to_markdown(epub_file, output_dir, output_format='pdf')
    
    # 查找生成的PDF文件
    pdf_found = False
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                pdf_found = True
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
                    
    return pdf_found

def main():
    parser = argparse.ArgumentParser(
        description='epub2any - 统一的EPUB转换工具，支持转换为Markdown、HTML、PDF格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s book.epub output_folder --format md     # 转换为Markdown
  %(prog)s book.epub output_folder --format html   # 转换为HTML
  %(prog)s book.epub output_folder --format pdf    # 转换为PDF
  %(prog)s book.epub output_folder --debug-pdf     # 调试PDF生成
        """
    )
    
    parser.add_argument(
        'epub_file', 
        type=str, 
        help='EPUB文件路径'
    )
    
    parser.add_argument(
        'output_folder', 
        type=str, 
        help='输出文件夹名称'
    )
    
    parser.add_argument(
        '--format', 
        type=str, 
        default='md', 
        choices=['md', 'html', 'pdf'], 
        help="输出格式: 'md' (Markdown), 'html' (HTML), 'pdf' (PDF)。默认为 'md'"
    )
    
    parser.add_argument(
        '--debug-pdf', 
        action='store_true', 
        help='调试PDF生成过程，显示详细的PDF内容分析'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='epub2any 1.0.0'
    )
    
    args = parser.parse_args()
    
    # 验证输入文件
    if not os.path.exists(args.epub_file):
        print(f"错误: EPUB文件不存在: {args.epub_file}")
        sys.exit(1)
        
    if not args.epub_file.lower().endswith('.epub'):
        print("错误: 请提供有效的.epub文件")
        sys.exit(1)
        
    if not args.output_folder:
        print("错误: 请提供输出文件夹名称")
        sys.exit(1)
    
    # 执行转换或调试
    try:
        if args.debug_pdf:
            print(f"调试模式: 分析EPUB文件 '{args.epub_file}' 的PDF生成过程")
            success = debug_pdf_generation(args.epub_file, args.output_folder)
            if success:
                print("\n✓ PDF调试完成")
            else:
                print("\n✗ PDF调试失败")
                sys.exit(1)
        else:
            print(f"转换EPUB文件 '{args.epub_file}' 为 {args.format.upper()} 格式...")
            epub_to_markdown(args.epub_file, args.output_folder, args.format)
            print(f"\n✓ 转换完成! 输出保存在: {args.output_folder}")
            
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()