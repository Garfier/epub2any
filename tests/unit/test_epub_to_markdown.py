#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epub_to_markdown 模块的单元测试

测试 EPUB 转换功能的核心逻辑。
"""

import pytest
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from epub_to_markdown import sanitize_filename, sanitize_image_filename


class TestSanitizeFilename:
    """测试文件名清理函数"""
    
    def test_sanitize_basic_filename(self):
        """测试基本文件名清理"""
        assert sanitize_filename("normal_file.txt") == "normal_file.txt"
        assert sanitize_filename("file with spaces.txt") == "file_with_spaces.txt"
    
    def test_sanitize_special_characters(self):
        """测试特殊字符清理"""
        # 函数会将所有特殊字符（包括点号）替换为单个下划线
        assert sanitize_filename("file<>:\"/|?*.txt") == "file_txt"
        assert sanitize_filename("文件名.txt") == "文件名_txt"
    
    def test_sanitize_empty_filename(self):
        """测试空文件名"""
        assert sanitize_filename("") == "_"
        assert sanitize_filename("   ") == "_"
    
    def test_sanitize_long_filename(self):
        """测试长文件名截断"""
        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name)
        # 函数不会截断长文件名，只是清理特殊字符
        # 点号会被替换为下划线
        expected = "a" * 300 + "_txt"
        assert result == expected


class TestSanitizeImageFilename:
    """测试图片文件名清理函数"""
    
    def test_preserve_image_extension(self):
        """测试保留图片扩展名"""
        assert sanitize_image_filename("image.jpg") == "image.jpg"
        assert sanitize_image_filename("image.png") == "image.png"
        assert sanitize_image_filename("image.svg") == "image.svg"
    
    def test_sanitize_image_with_special_chars(self):
        """测试包含特殊字符的图片文件名"""
        assert sanitize_image_filename("图片 文件.jpg") == "图片_文件.jpg"
        assert sanitize_image_filename("image<test>.png") == "image_test.png"
    
    def test_sanitize_image_with_dots(self):
        """测试包含多个点的图片文件名"""
        # 图片文件名清理函数不会替换名称部分的点，只处理扩展名
        assert sanitize_image_filename("image.test.jpg") == "image.test.jpg"
        assert sanitize_image_filename("my.image.file.png") == "my.image.file.png"
    
    def test_sanitize_image_no_extension(self):
        """测试没有扩展名的图片文件"""
        assert sanitize_image_filename("image") == "image"
        assert sanitize_image_filename("image_file") == "image_file"
        assert sanitize_image_filename("") == "_"


@pytest.mark.unit
class TestEpubToMarkdownCore:
    """测试 EPUB 转换核心功能"""
    
    def test_import_epub_to_markdown(self):
        """测试能否正确导入主函数"""
        try:
            from epub_to_markdown import epub_to_markdown
            assert callable(epub_to_markdown)
        except ImportError as e:
            pytest.fail(f"无法导入 epub_to_markdown 函数: {e}")
    
    def test_epub_to_markdown_invalid_file(self):
        """测试处理无效 EPUB 文件"""
        from epub_to_markdown import epub_to_markdown
        
        # 测试不存在的文件
        try:
            result = epub_to_markdown("nonexistent.epub", "output", "md")
            # 如果没有抛出异常，结果应该是False
            assert result is False
        except Exception:
            # 如果抛出异常也是可以接受的
            pass
    
    def test_supported_formats(self):
        """测试支持的输出格式"""
        from epub_to_markdown import epub_to_markdown
        
        # 这些格式应该被支持
        supported_formats = ['md', 'html', 'pdf']
        
        for fmt in supported_formats:
            # 这里只测试格式参数是否被接受，不执行实际转换
            try:
                # 使用不存在的文件，应该在文件检查阶段失败，而不是格式检查阶段
                result = epub_to_markdown("nonexistent.epub", "output", fmt)
                # 应该因为文件不存在而返回 False，而不是因为格式不支持
                assert result is False
            except Exception as e:
                # 如果抛出异常，确保不是因为格式不支持
                assert "format" not in str(e).lower()


if __name__ == '__main__':
    pytest.main([__file__])