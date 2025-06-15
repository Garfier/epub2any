# EPUB2Any 测试文档

本文档描述了 epub2any 项目的测试结构和使用方法。

## 测试结构

```
tests/
├── __init__.py                 # 测试包初始化
├── conftest.py                 # pytest 配置和 fixtures
├── README.md                   # 本文档
├── unit/                       # 单元测试
│   ├── __init__.py
│   └── test_epub_to_markdown.py
├── integration/                # 集成测试
│   ├── __init__.py
│   ├── test_epub2any_integration.py
│   ├── test_image_optimization.py
│   ├── test_pdf_navigation.py
│   └── debug_pdf_toc.py
├── test_data/                  # 测试数据
│   ├── __init__.py
│   ├── create_test_epub.py
│   └── create_test_epub_with_images.py
└── utils/                      # 测试工具
    ├── __init__.py
    └── test_output_manager.py
```

## 测试类型

### 单元测试 (Unit Tests)

位于 `tests/unit/` 目录，测试单个函数或类的功能：

- `test_epub_to_markdown.py`: 测试核心转换函数
- 测试文件名清理函数
- 测试图片文件名处理函数

### 集成测试 (Integration Tests)

位于 `tests/integration/` 目录，测试完整的功能流程：

- `test_epub2any_integration.py`: 测试完整的转换流程
- `test_image_optimization.py`: 测试图片优化功能
- `test_pdf_navigation.py`: 测试PDF导航功能
- `debug_pdf_toc.py`: PDF目录调试工具

### 测试数据

位于 `tests/test_data/` 目录，包含测试用的数据生成脚本：

- `create_test_epub.py`: 生成基本测试EPUB文件
- `create_test_epub_with_images.py`: 生成包含图片的测试EPUB文件

### 测试工具

位于 `tests/utils/` 目录，包含测试辅助工具：

- `test_output_manager.py`: 管理和清理测试输出文件

## 运行测试

### 使用测试运行脚本（推荐）

```bash
# 安装测试依赖
python3 run_tests.py setup --install-deps

# 运行所有测试
python3 run_tests.py all

# 运行单元测试
python3 run_tests.py unit

# 运行集成测试
python3 run_tests.py integration

# 运行快速测试（排除慢速测试）
python3 run_tests.py fast

# 运行测试并生成覆盖率报告
python3 run_tests.py all --coverage

# 详细输出
python3 run_tests.py all -v

# 清理测试输出
python3 run_tests.py clean
```

### 直接使用 pytest

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行特定测试文件
pytest tests/unit/test_epub_to_markdown.py

# 运行特定测试函数
pytest tests/unit/test_epub_to_markdown.py::TestSanitizeFilename::test_sanitize_basic_filename

# 详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=. --cov-report=html

# 排除慢速测试
pytest -m "not slow"

# 只运行特定标记的测试
pytest -m "unit"
pytest -m "integration"
pytest -m "images"
```

## 测试标记

项目使用 pytest 标记来分类测试：

- `@pytest.mark.unit`: 单元测试
- `@pytest.mark.integration`: 集成测试
- `@pytest.mark.slow`: 慢速测试
- `@pytest.mark.pdf`: PDF相关测试
- `@pytest.mark.html`: HTML相关测试
- `@pytest.mark.markdown`: Markdown相关测试
- `@pytest.mark.images`: 图片处理相关测试

## 测试数据管理

### 生成测试数据

```bash
# 生成基本测试EPUB
python3 tests/test_data/create_test_epub.py

# 生成包含图片的测试EPUB
python3 tests/test_data/create_test_epub_with_images.py
```

### 清理测试输出

```bash
# 列出所有测试输出目录
python3 tests/utils/test_output_manager.py list

# 清理所有测试输出目录
python3 tests/utils/test_output_manager.py clean

# 强制清理（不需要确认）
python3 tests/utils/test_output_manager.py clean --force
```

## 添加新测试

### 添加单元测试

1. 在 `tests/unit/` 目录下创建新的测试文件
2. 文件名以 `test_` 开头
3. 导入要测试的模块
4. 创建测试类和测试函数
5. 使用 `@pytest.mark.unit` 标记

### 添加集成测试

1. 在 `tests/integration/` 目录下创建新的测试文件
2. 使用 `@pytest.mark.integration` 和 `@pytest.mark.slow` 标记
3. 使用 fixtures 获取测试数据和临时目录
4. 测试完整的功能流程

### 使用 Fixtures

项目提供了以下 fixtures：

- `project_root_dir`: 项目根目录
- `test_data_dir`: 测试数据目录
- `temp_output_dir`: 临时输出目录（自动清理）
- `sample_epub_file`: 示例EPUB文件
- `sample_epub_with_images_file`: 包含图片的示例EPUB文件

## 持续集成

测试结构支持在CI/CD环境中运行：

```bash
# CI环境中的测试命令
python3 run_tests.py setup --install-deps
python3 run_tests.py all --coverage
```

## 故障排除

### 常见问题

1. **测试依赖缺失**
   ```bash
   python3 run_tests.py setup --install-deps
   ```

2. **测试数据缺失**
   ```bash
   python3 run_tests.py setup
   ```

3. **测试输出目录冲突**
   ```bash
   python3 run_tests.py clean
   ```

4. **权限问题**
   ```bash
   chmod +x run_tests.py
   chmod +x tests/utils/test_output_manager.py
   ```

### 调试测试

```bash
# 运行单个测试并显示详细输出
pytest tests/unit/test_epub_to_markdown.py::TestSanitizeFilename::test_sanitize_basic_filename -v -s

# 进入调试模式
pytest --pdb

# 在第一个失败处停止
pytest -x
```

## 最佳实践

1. **测试隔离**: 每个测试应该独立运行，不依赖其他测试的结果
2. **使用临时目录**: 使用 `temp_output_dir` fixture 避免测试文件冲突
3. **清理资源**: 测试结束后自动清理临时文件
4. **有意义的断言**: 使用清晰的断言消息
5. **测试边界条件**: 测试正常情况、边界情况和错误情况
6. **使用标记**: 合理使用pytest标记来分类测试

## 贡献指南

在提交代码前，请确保：

1. 所有测试通过
2. 新功能有对应的测试
3. 测试覆盖率不降低
4. 遵循项目的测试结构和命名约定