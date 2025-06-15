#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
from ebooklib import epub
import base64

def create_simple_svg_image(color, text):
    """Create a simple SVG image with specified color and text"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="100" fill="{color}"/>
  <text x="100" y="50" font-family="Arial" font-size="16" fill="white" text-anchor="middle" dominant-baseline="middle">{text}</text>
</svg>'''
    return svg_content.encode('utf-8')

def create_simple_png_data():
    """Create a simple PNG image data (1x1 pixel red)"""
    # This is a base64 encoded 1x1 red pixel PNG
    png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    return base64.b64decode(png_base64)

def create_test_epub_with_images():
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-book-with-images')
    book.set_title('测试书籍（含图片）')
    book.set_language('zh')
    book.add_author('测试作者')
    
    # Create images
    # SVG image
    svg_image = epub.EpubImage()
    svg_image.id = 'image1'
    svg_image.file_name = 'images/test-image.svg'
    svg_image.media_type = 'image/svg+xml'
    svg_image.content = create_simple_svg_image('#4CAF50', '图片1')
    book.add_item(svg_image)
    
    # PNG image with special characters in filename
    png_image = epub.EpubImage()
    png_image.id = 'image2'
    png_image.file_name = 'images/特殊字符 图片.png'
    png_image.media_type = 'image/png'
    png_image.content = create_simple_png_data()
    book.add_item(png_image)
    
    # Another SVG with dots and spaces in filename
    svg_image2 = epub.EpubImage()
    svg_image2.id = 'image3'
    svg_image2.file_name = 'images/test.image.with.dots.svg'
    svg_image2.media_type = 'image/svg+xml'
    svg_image2.content = create_simple_svg_image('#2196F3', '图片3')
    book.add_item(svg_image2)
    
    # Create chapters with images
    chapter1 = epub.EpubHtml(title='第一章：图片展示', file_name='chapter1.xhtml', lang='zh')
    chapter1.content = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head><title>第一章：图片展示</title></head>
    <body>
        <h1>第一章：图片展示</h1>
        <p>这是第一章的内容，包含一些图片。</p>
        <h2>SVG图片示例</h2>
        <p>下面是一个SVG图片：</p>
        <img src="images/test-image.svg" alt="测试SVG图片" />
        <h2>PNG图片示例</h2>
        <p>下面是一个PNG图片：</p>
        <img src="images/特殊字符 图片.png" alt="特殊字符PNG图片" />
    </body>
    </html>
    '''
    book.add_item(chapter1)
    
    chapter2 = epub.EpubHtml(title='第二章：更多图片', file_name='chapter2.xhtml', lang='zh')
    chapter2.content = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head><title>第二章：更多图片</title></head>
    <body>
        <h1>第二章：更多图片</h1>
        <p>这是第二章的内容。</p>
        <h2>带点号的文件名</h2>
        <p>下面是一个文件名包含点号的图片：</p>
        <img src="images/test.image.with.dots.svg" alt="带点号的SVG图片" />
        <p>这个图片的原始文件名是：test.image.with.dots.svg</p>
    </body>
    </html>
    '''
    book.add_item(chapter2)
    
    # Define Table of Contents
    book.toc = (
        epub.Link("chapter1.xhtml", "第一章：图片展示", "chapter1"),
        epub.Link("chapter2.xhtml", "第二章：更多图片", "chapter2"),
    )
    
    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = 'body { font-family: Arial, sans-serif; margin: 40px; }'
    nav_css = epub.EpubItem(uid="nav_css", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Basic spine
    book.spine = ['nav', chapter1, chapter2]
    
    # Write to file
    epub.write_epub('test_with_images.epub', book, {})
    print("Created test_with_images.epub with sample images")
    print("Images included:")
    print("  - test-image.svg")
    print("  - 特殊字符 图片.png")
    print("  - test.image.with.dots.svg")

if __name__ == '__main__':
    create_test_epub_with_images()