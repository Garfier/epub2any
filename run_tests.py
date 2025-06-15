#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本

提供便捷的测试执行方式，支持不同类型的测试运行。
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def install_test_dependencies():
    """安装测试依赖"""
    print("安装测试依赖...")
    
    # 检查是否已安装 pytest
    try:
        import pytest
        print("✓ pytest 已安装")
    except ImportError:
        print("安装 pytest...")
        if not run_command([sys.executable, '-m', 'pip', 'install', 'pytest']):
            print("✗ pytest 安装失败")
            return False
    
    # 检查是否已安装 pytest-cov
    try:
        import pytest_cov
        print("✓ pytest-cov 已安装")
    except ImportError:
        print("安装 pytest-cov...")
        if not run_command([sys.executable, '-m', 'pip', 'install', 'pytest-cov']):
            print("✗ pytest-cov 安装失败")
            return False
    
    return True


def run_unit_tests(verbose=False, coverage=False):
    """运行单元测试"""
    print("\n" + "=" * 50)
    print("运行单元测试")
    print("=" * 50)
    
    cmd = [sys.executable, '-m', 'pytest', 'tests/unit']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=term-missing'])
    
    return run_command(cmd)


def run_integration_tests(verbose=False):
    """运行集成测试"""
    print("\n" + "=" * 50)
    print("运行集成测试")
    print("=" * 50)
    
    cmd = [sys.executable, '-m', 'pytest', 'tests/integration']
    
    if verbose:
        cmd.append('-v')
    
    return run_command(cmd)


def run_all_tests(verbose=False, coverage=False):
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("运行所有测试")
    print("=" * 50)
    
    cmd = [sys.executable, '-m', 'pytest', 'tests']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=term-missing', '--cov-report=html'])
    
    return run_command(cmd)


def run_fast_tests(verbose=False):
    """运行快速测试（排除慢速测试）"""
    print("\n" + "=" * 50)
    print("运行快速测试")
    print("=" * 50)
    
    cmd = [sys.executable, '-m', 'pytest', 'tests', '-m', 'not slow']
    
    if verbose:
        cmd.append('-v')
    
    return run_command(cmd)


def clean_test_outputs():
    """清理测试输出"""
    print("\n" + "=" * 50)
    print("清理测试输出")
    print("=" * 50)
    
    try:
        from tests.utils.test_output_manager import TestOutputManager
        manager = TestOutputManager()
        return manager.clean_test_outputs(confirm=False)
    except ImportError:
        print("无法导入测试输出管理器")
        return False


def generate_test_data():
    """生成测试数据"""
    print("\n" + "=" * 50)
    print("生成测试数据")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # 生成基本测试 EPUB
    if not (project_root / "test.epub").exists():
        print("生成基本测试 EPUB...")
        cmd = [sys.executable, 'tests/test_data/create_test_epub.py']
        if not run_command(cmd, cwd=project_root):
            print("✗ 基本测试 EPUB 生成失败")
            return False
        print("✓ 基本测试 EPUB 生成成功")
    else:
        print("✓ 基本测试 EPUB 已存在")
    
    # 生成带图片的测试 EPUB
    if not (project_root / "test_with_images.epub").exists():
        print("生成带图片的测试 EPUB...")
        cmd = [sys.executable, 'tests/test_data/create_test_epub_with_images.py']
        if not run_command(cmd, cwd=project_root):
            print("✗ 带图片的测试 EPUB 生成失败")
            return False
        print("✓ 带图片的测试 EPUB 生成成功")
    else:
        print("✓ 带图片的测试 EPUB 已存在")
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='epub2any 测试运行脚本')
    parser.add_argument('test_type', nargs='?', default='all',
                       choices=['unit', 'integration', 'all', 'fast', 'clean', 'setup'],
                       help='测试类型')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='详细输出')
    parser.add_argument('--coverage', action='store_true',
                       help='生成覆盖率报告')
    parser.add_argument('--install-deps', action='store_true',
                       help='安装测试依赖')
    
    args = parser.parse_args()
    
    # 切换到项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    success = True
    
    # 安装依赖
    if args.install_deps:
        if not install_test_dependencies():
            return 1
    
    # 设置测试环境
    if args.test_type == 'setup':
        success = generate_test_data()
    
    # 清理测试输出
    elif args.test_type == 'clean':
        success = clean_test_outputs()
    
    # 运行测试
    else:
        # 确保测试数据存在
        if not generate_test_data():
            return 1
        
        if args.test_type == 'unit':
            success = run_unit_tests(args.verbose, args.coverage)
        elif args.test_type == 'integration':
            success = run_integration_tests(args.verbose)
        elif args.test_type == 'fast':
            success = run_fast_tests(args.verbose)
        else:  # all
            success = run_all_tests(args.verbose, args.coverage)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())