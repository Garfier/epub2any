#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 配置文件

定义测试的全局配置、fixtures 和钩子函数。
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_dir():
    """项目根目录 fixture"""
    return project_root


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录 fixture"""
    return project_root / "tests" / "test_data"


@pytest.fixture(scope="function")
def temp_output_dir():
    """临时输出目录 fixture
    
    为每个测试函数创建一个临时目录，测试结束后自动清理。
    """
    temp_dir = tempfile.mkdtemp(prefix="epub2any_test_")
    yield Path(temp_dir)
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def sample_epub_file(test_data_dir):
    """示例 EPUB 文件 fixture
    
    如果不存在则创建一个测试用的 EPUB 文件。
    """
    epub_file = project_root / "test.epub"
    
    if not epub_file.exists():
        # 导入并运行测试数据生成脚本
        sys.path.insert(0, str(test_data_dir))
        from create_test_epub import create_test_epub
        create_test_epub(str(epub_file))
    
    return epub_file


@pytest.fixture(scope="session")
def sample_epub_with_images_file(test_data_dir):
    """带图片的示例 EPUB 文件 fixture"""
    epub_file = project_root / "test_with_images.epub"
    
    if not epub_file.exists():
        # 导入并运行测试数据生成脚本
        sys.path.insert(0, str(test_data_dir))
        from create_test_epub_with_images import create_test_epub_with_images
        create_test_epub_with_images()
    
    return epub_file


@pytest.fixture(autouse=True)
def setup_test_environment():
    """设置测试环境
    
    在每个测试前后执行的设置和清理操作。
    """
    # 测试前设置
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    yield
    
    # 测试后清理
    os.chdir(original_cwd)


def pytest_configure(config):
    """pytest 配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集项"""
    # 为集成测试添加 slow 标记
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)