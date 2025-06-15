#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试输出管理工具

用于管理和清理测试过程中生成的输出文件和目录。
"""

import os
import shutil
import glob
from pathlib import Path


class TestOutputManager:
    """测试输出管理器"""
    
    def __init__(self, base_dir=None):
        """初始化测试输出管理器
        
        Args:
            base_dir: 基础目录，默认为项目根目录
        """
        if base_dir is None:
            # 获取项目根目录（tests的父目录）
            self.base_dir = Path(__file__).parent.parent.parent
        else:
            self.base_dir = Path(base_dir)
    
    def get_test_output_dirs(self):
        """获取所有测试输出目录
        
        Returns:
            list: 测试输出目录列表
        """
        patterns = [
            'test_*',
            'output*',
            '*_test',
            '*_output'
        ]
        
        test_dirs = []
        for pattern in patterns:
            test_dirs.extend(glob.glob(str(self.base_dir / pattern)))
        
        # 过滤掉tests目录本身
        test_dirs = [d for d in test_dirs if not d.endswith('/tests')]
        
        return sorted(test_dirs)
    
    def clean_test_outputs(self, confirm=True):
        """清理所有测试输出目录
        
        Args:
            confirm: 是否需要确认
        
        Returns:
            bool: 是否成功清理
        """
        test_dirs = self.get_test_output_dirs()
        
        if not test_dirs:
            print("没有找到测试输出目录")
            return True
        
        print(f"找到 {len(test_dirs)} 个测试输出目录:")
        for i, dir_path in enumerate(test_dirs, 1):
            print(f"  {i}. {os.path.basename(dir_path)}")
        
        if confirm:
            response = input("\n是否删除这些目录? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("取消清理操作")
                return False
        
        success_count = 0
        for dir_path in test_dirs:
            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"✓ 已删除: {os.path.basename(dir_path)}")
                    success_count += 1
            except Exception as e:
                print(f"✗ 删除失败 {os.path.basename(dir_path)}: {e}")
        
        print(f"\n清理完成: {success_count}/{len(test_dirs)} 个目录")
        return success_count == len(test_dirs)
    
    def create_test_output_dir(self, name):
        """创建测试输出目录
        
        Args:
            name: 目录名称
        
        Returns:
            Path: 创建的目录路径
        """
        output_dir = self.base_dir / name
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def list_test_outputs(self):
        """列出所有测试输出目录的详细信息"""
        test_dirs = self.get_test_output_dirs()
        
        if not test_dirs:
            print("没有找到测试输出目录")
            return
        
        print(f"测试输出目录列表 (共 {len(test_dirs)} 个):")
        print("-" * 60)
        
        for dir_path in test_dirs:
            dir_name = os.path.basename(dir_path)
            try:
                # 获取目录大小
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                
                size_mb = total_size / (1024 * 1024)
                print(f"{dir_name:<30} {file_count:>6} 文件 {size_mb:>8.2f} MB")
            except Exception as e:
                print(f"{dir_name:<30} {'错误':>6} {str(e)[:20]:>8}")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='测试输出管理工具')
    parser.add_argument('action', choices=['list', 'clean'], 
                       help='操作类型: list(列出) 或 clean(清理)')
    parser.add_argument('--force', action='store_true', 
                       help='强制清理，不需要确认')
    
    args = parser.parse_args()
    
    manager = TestOutputManager()
    
    if args.action == 'list':
        manager.list_test_outputs()
    elif args.action == 'clean':
        manager.clean_test_outputs(confirm=not args.force)


if __name__ == '__main__':
    main()