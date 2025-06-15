#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epub2any 集成测试

测试完整的 EPUB 转换流程，包括所有输出格式。
"""

import pytest
import os
import sys
import subprocess
import shutil
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.mark.integration
@pytest.mark.slow
class TestEpub2AnyIntegration:
    """epub2any 集成测试类"""
    
    def test_epub2any_help(self):
        """测试 epub2any 帮助信息"""
        result = subprocess.run(
            ['python3', 'epub2any.py', '--help'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent
        )
        
        assert result.returncode == 0
        assert 'epub2any' in result.stdout
        assert 'EPUB file to convert' in result.stdout
    
    def test_epub2any_version(self):
        """测试 epub2any 版本信息"""
        result = subprocess.run(
            ['python3', 'epub2any.py', '--version'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent
        )
        
        assert result.returncode == 0
        assert 'epub2any' in result.stdout
    
    def test_markdown_conversion(self, sample_epub_file, temp_output_dir):
        """测试 Markdown 格式转换"""
        output_dir = temp_output_dir / "test_md"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_file),
            str(output_dir),
            '--format', 'md'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        assert result.returncode == 0
        assert output_dir.exists()
        
        # 检查是否生成了 Markdown 文件
        md_files = list(output_dir.rglob('*.md'))
        assert len(md_files) > 0
    
    def test_html_conversion(self, sample_epub_file, temp_output_dir):
        """测试 HTML 格式转换"""
        output_dir = temp_output_dir / "test_html"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_file),
            str(output_dir),
            '--format', 'html'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        assert result.returncode == 0
        assert output_dir.exists()
        
        # 检查是否生成了 HTML 文件
        html_files = list(output_dir.rglob('*.html'))
        assert len(html_files) > 0
    
    def test_pdf_conversion(self, sample_epub_file, temp_output_dir):
        """测试 PDF 格式转换"""
        output_dir = temp_output_dir / "test_pdf"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_file),
            str(output_dir),
            '--format', 'pdf'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        assert result.returncode == 0
        assert output_dir.exists()
        
        # 检查是否生成了 PDF 文件
        pdf_files = list(output_dir.rglob('*.pdf'))
        assert len(pdf_files) > 0
    
    def test_image_handling(self, sample_epub_with_images_file, temp_output_dir):
        """测试图片处理功能"""
        # 测试 Markdown 格式的图片处理
        md_output = temp_output_dir / "test_images_md"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_with_images_file),
            str(md_output),
            '--format', 'md'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        assert result.returncode == 0
        
        # 检查是否创建了 images 目录
        images_dirs = list(md_output.rglob('images'))
        assert len(images_dirs) > 0
        
        # 检查图片文件是否存在
        for images_dir in images_dirs:
            if images_dir.is_dir():
                image_files = list(images_dir.glob('*'))
                if image_files:  # 如果有图片文件
                    # 检查扩展名是否保留
                    for img_file in image_files:
                        assert img_file.suffix in ['.svg', '.png', '.jpg', '.jpeg', '.gif']
    
    def test_pdf_debug_mode(self, sample_epub_file, temp_output_dir):
        """测试 PDF 调试模式"""
        output_dir = temp_output_dir / "test_pdf_debug"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_file),
            str(output_dir),
            '--format', 'pdf',
            '--debug-pdf'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        assert result.returncode == 0
        assert output_dir.exists()
    
    def test_invalid_format(self, sample_epub_file, temp_output_dir):
        """测试无效的输出格式"""
        output_dir = temp_output_dir / "test_invalid"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            str(sample_epub_file),
            str(output_dir),
            '--format', 'invalid'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        # 应该返回非零退出码
        assert result.returncode != 0
    
    def test_nonexistent_epub(self, temp_output_dir):
        """测试不存在的 EPUB 文件"""
        output_dir = temp_output_dir / "test_nonexistent"
        
        result = subprocess.run([
            'python3', 'epub2any.py',
            'nonexistent.epub',
            str(output_dir),
            '--format', 'md'
        ], capture_output=True, text=True,
           cwd=Path(__file__).parent.parent.parent)
        
        # 应该返回非零退出码
        assert result.returncode != 0


if __name__ == '__main__':
    pytest.main([__file__])