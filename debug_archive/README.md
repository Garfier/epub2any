# 调试文件整理说明

## debug_archive/
包含开发过程中创建的调试和修复脚本：
- analyze_pdf_pages.py - PDF页面内容分析脚本
- check_pdf_simple.py - 简单PDF检查脚本
- debug_pdf_links.py - PDF链接调试脚本
- debug_pdf_toc.py - PDF目录调试脚本
- fix_bookmark_pages.py - 书签页码修复脚本
- fix_pdf_navigation.py - PDF导航修复脚本
- test_bookmark_fix.py - 书签修复测试脚本
- test_bookmark_navigation.py - 书签导航测试脚本
- test_pdf_navigation.py - PDF导航测试脚本
- test_pdf_navigation_fix.py - PDF导航修复测试脚本
- epub_to_markdown.py.backup - 主程序备份文件

## temp_outputs/
包含测试和调试过程中生成的临时输出：
- debug_links/ - 链接调试输出
- test_final/ - 最终测试输出
- test_navigation_fix/ - 导航修复测试输出
- test_output/ - 通用测试输出

## 清理内容
- 删除了所有 __pycache__ 目录
- 删除了 .pytest_cache 目录
- 整理了散落在根目录的调试文件

这些文件已被整理但保留，以备将来参考或需要时使用。
