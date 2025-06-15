# EPUB to Any Format Converter

`epub2any` 是一个功能强大的Python工具，用于将EPUB电子书转换为多种格式，包括Markdown、HTML和PDF，具有高级导航功能和完善的调试支持。

## 📁 项目结构

```
epub2any/
├── epub_to_markdown.py     # 核心转换程序
├── epub2any.py            # 统一命令行入口
├── requirements.txt       # 依赖包列表
├── tests/                 # 正式测试套件
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── test_data/        # 测试数据
├── convert/outputs/       # 转换输出目录
├── debug_archive/         # 调试文件归档
└── temp_outputs/          # 临时输出归档
```

## 功能特性

- 🔄 **多格式转换**: 支持转换为Markdown、HTML、PDF格式
- 🖼️ **智能图片处理**: 提取并保留EPUB中的图片，智能处理文件名
- 📚 **PDF增强功能**: 生成带交互式目录和书签的PDF文件
- 🔗 **章节导航**: 支持PDF中的章节跳转和导航
- 📄 **自动页码**: PDF输出中的自动页面编号
- 🌐 **HTML内嵌**: HTML格式支持base64图片内嵌
- 🔍 **调试模式**: 提供PDF生成过程的详细分析
- 📁 **文件管理**: 跨平台兼容的文件名处理
- 🔗 **链接保持**: 处理内部链接和引用

## 安装要求

- Python 3.6+
- 必需的Python包（通过 `pip install -r requirements.txt` 安装）:
  - ebooklib
  - beautifulsoup4
  - html2text
  - pyppeteer
  - xhtml2pdf
  - **PyPDF2** (用于PDF书签和导航功能)

## 安装步骤

1. 克隆仓库:
```bash
git clone git@github.com:Garfier/epub2any.git
cd epub2any
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

**提示**: 首次使用PDF功能时，可能需要运行 `pyppeteer-install` 来安装Chromium浏览器。

## 使用方法

### 统一命令行工具 (推荐)

```bash
python3 epub2any.py <epub_file> <output_folder> [选项]
```

#### 命令行参数

- `epub_file`: EPUB文件路径
- `output_folder`: 输出文件夹名称
- `--format {md,html,pdf}`: 输出格式（默认: md）
- `--debug-pdf`: 调试PDF生成过程
- `--version`: 显示版本信息
- `--help`: 显示帮助信息

### 直接使用核心转换程序

```bash
python epub_to_markdown.py <epub_file> <output_directory> [--format FORMAT]
```

### 使用示例

#### 1. 转换为Markdown格式

```bash
# 使用统一工具
python3 epub2any.py book.epub output_md --format md

# 或使用核心程序
python epub_to_markdown.py book.epub output/
```

#### 2. 转换为HTML格式

```bash
# 使用统一工具
python3 epub2any.py book.epub output_html --format html

# 或使用核心程序
python epub_to_markdown.py book.epub output/ --format html
```

#### 3. 转换为PDF格式（带导航功能）

```bash
# 使用统一工具
python3 epub2any.py book.epub output_pdf --format pdf

# 或使用核心程序
python epub_to_markdown.py book.epub output/ --format pdf
```

#### 4. 调试PDF生成

```bash
python3 epub2any.py book.epub debug_output --debug-pdf
```

## 输出结构

### Markdown格式输出
```
output_md/
└── 书名/
    ├── 000_章节1.md
    ├── 001_章节2.md
    ├── ...
    └── images/
        ├── image1.png
        ├── image2.svg
        └── ...
```
- 每个章节生成独立的 `.md` 文件
- `images/` 目录包含提取的图片
- 保留章节间的内部链接
- 适合编辑和版本控制

### HTML格式输出
```
output_html/
└── 书名/
    ├── 书名.html          # 包含base64内嵌图片
    ├── 书名.pdf           # 自动生成的PDF
    └── images/
        ├── image1.png     # 独立的图片文件
        ├── image2.svg
        └── ...
```
- 单个HTML文件，包含嵌入式CSS
- 图片采用base64编码内嵌
- 同时保留独立图片文件
- 自包含，易于分享
- 针对可读性优化的样式

### PDF格式输出
```
output_pdf/
└── 书名/
    ├── 书名.pdf           # 带书签的PDF文件
    └── images/
        ├── image1.png     # 提取的图片文件
        ├── image2.svg
        └── ...
```
- 单个PDF文件包含所有内容
- **📖 开头自动生成交互式目录**
- **🔗 可点击的章节链接，便于导航**
- **📑 PDF书签/大纲，快速跳转**
- **📄 页眉/页脚中的页码**
- 保留格式和图片
- 优化的排版和布局

## 图片处理优化

### 智能文件名处理

- ✅ 保留原始扩展名（.png, .jpg, .svg等）
- ✅ 安全处理特殊字符（空格转下划线）
- ✅ 支持复杂文件名（如：`test.image.with.dots.svg`）

### 文件名转换示例

| 原始文件名 | 处理后文件名 |
|------------|-------------|
| `特殊字符 图片.png` | `特殊字符_图片.png` |
| `test.image.with.dots.svg` | `test.image.with.dots.svg` |
| `test-image.svg` | `test-image.svg` |

## 格式特性对比

| 格式 | 图片处理 | 文件结构 | 特殊功能 |
|------|----------|----------|----------|
| **Markdown** | 独立文件 + 相对路径 | 多个.md文件 | 适合编辑和版本控制 |
| **HTML** | base64内嵌 + 独立文件 | 单个.html文件 | 自包含，易于分享 |
| **PDF** | 内嵌 + 独立文件 | 单个.pdf文件 | 带书签导航 |

## PDF导航功能详解

### 交互式目录
- 从EPUB章节结构自动生成
- 可点击链接跳转到特定章节
- 清洁、专业的格式

### PDF书签
- 浏览器风格的导航面板
- 分层的章节结构
- 一键跳转到任何部分

### 页面编号
- 整个文档的一致页码
- 页眉/页脚中的导航信息

### 内部链接
- 所有交叉引用保持功能
- 相关部分间的平滑导航
- 使用唯一ID增强PDF内部链接

## 功能详解

### 图片处理
- 从EPUB文件中提取图片
- 将图片转换为Web兼容格式
- 更新转换内容中的图片引用
- 智能文件名处理，保持原始扩展名

### 链接处理
- 保留章节间的内部链接
- 为目标格式更新链接引用
- 维护文档结构和导航
- 增强的PDF内部链接功能

### 文件名清理
- 移除或替换无效字符
- 确保跨平台兼容性
- 保留有意义的文件名

## 测试和调试

### 测试PDF导航功能

```bash
# 使用统一工具进行调试
python3 epub2any.py your_book.epub test_output --debug-pdf
```

**调试信息包括:**
- PDF文件大小和页数
- 书签列表
- 第一页内容分析
- 目录和章节检测

### 运行测试套件

```bash
# 运行所有测试
python run_tests.py

# 运行特定测试
python -m pytest tests/integration/test_pdf_navigation.py
```

## 故障排除

### 常见问题

1. **缺少依赖**: 确保所有必需的包都已安装
2. **权限错误**: 确保输出目录有写入权限
3. **大文件**: 大型EPUB文件的PDF转换可能需要时间
4. **PyPDF2未找到**: 使用 `pip install PyPDF2` 安装书签功能
5. **Chromium未安装**: 运行 `pyppeteer-install` 安装浏览器

### 错误信息

- "No items found in EPUB": EPUB文件可能损坏或为空
- "Failed to extract images": 检查EPUB是否包含有效的图片文件
- "PDF generation failed": 确保pyppeteer正确安装
- "PyPDF2 not available": 将跳过书签，但仍会生成PDF

### 错误处理

工具包含完善的错误处理机制：
- 文件存在性检查
- EPUB格式验证
- 依赖包检查
- 转换过程异常捕获

## 性能说明

- 带导航功能的PDF生成对于大型书籍可能需要更长时间
- 书签创建增加的开销很小
- 目录生成是自动且快速的
- 图片处理针对性能进行了优化

## 版本信息

当前版本: **1.0.0**

查看版本：
```bash
python3 epub2any.py --version
```

## 与原工具的关系

`epub2any.py` 是原有工具的统一入口：

- 整合了 `epub_to_markdown.py` 的转换功能
- 整合了调试功能
- 提供了更友好的命令行界面
- 保持了所有原有功能的兼容性

## 技术实现

- **EPUB解析**: 使用 `ebooklib` 库
- **HTML处理**: 使用 `BeautifulSoup4`
- **Markdown转换**: 使用 `html2text`
- **PDF生成**: 使用 `pyppeteer` (Chrome/Chromium)
- **PDF处理**: 使用 `PyPDF2` 添加书签
- **图片处理**: 智能文件名处理和格式转换
- **错误处理**: 完善的异常捕获和用户友好的错误信息

## 贡献

欢迎贡献！请随时提交Pull Request。

### 开发环境设置

1. Fork并克隆仓库
2. 安装开发依赖: `pip install -r requirements.txt`
3. 运行测试: `python run_tests.py`
4. 提交更改前确保所有测试通过

## 许可证

本项目是开源的，采用MIT许可证。