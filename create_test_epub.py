#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建一个简单的测试EPUB文件
"""

import os
import zipfile
from datetime import datetime

def create_test_epub(output_path="test.epub"):
    """
    创建一个包含多个章节的测试EPUB文件
    """
    
    # EPUB文件结构
    files = {
        'mimetype': 'application/epub+zip',
        
        'META-INF/container.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''',
        
        'OEBPS/content.opf': '''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>测试书籍</dc:title>
    <dc:creator>测试作者</dc:creator>
    <dc:identifier id="BookId">test-book-001</dc:identifier>
    <dc:language>zh-CN</dc:language>
    <dc:date>''' + datetime.now().strftime('%Y-%m-%d') + '''</dc:date>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="chapter2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
    <item id="chapter3" href="chapter3.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="chapter1"/>
    <itemref idref="chapter2"/>
    <itemref idref="chapter3"/>
  </spine>
</package>''',
        
        'OEBPS/toc.ncx': '''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="test-book-001"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>测试书籍</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel><text>第一章：开始</text></navLabel>
      <content src="chapter1.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-2" playOrder="2">
      <navLabel><text>第二章：发展</text></navLabel>
      <content src="chapter2.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-3" playOrder="3">
      <navLabel><text>第三章：结束</text></navLabel>
      <content src="chapter3.xhtml"/>
    </navPoint>
  </navMap>
</ncx>''',
        
        'OEBPS/chapter1.xhtml': '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>第一章：开始</title>
</head>
<body>
  <h1>第一章：开始</h1>
  <p>这是第一章的内容。在这一章中，我们将介绍故事的背景和主要人物。</p>
  <p>故事发生在一个美丽的小镇上，那里有着悠久的历史和丰富的文化。</p>
  <h2 id="section1-1">1.1 背景介绍</h2>
  <p>小镇位于山谷之中，四周环绕着青山绿水。</p>
  <h2 id="section1-2">1.2 主要人物</h2>
  <p>主人公是一个年轻的学者，对历史充满了浓厚的兴趣。</p>
</body>
</html>''',
        
        'OEBPS/chapter2.xhtml': '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>第二章：发展</title>
</head>
<body>
  <h1>第二章：发展</h1>
  <p>在第二章中，故事情节开始发展，主人公遇到了各种挑战和机遇。</p>
  <p>通过不断的努力和学习，主人公逐渐成长起来。</p>
  <h2 id="section2-1">2.1 遇到挑战</h2>
  <p>第一个挑战是解读古老的文献。</p>
  <h2 id="section2-2">2.2 寻找线索</h2>
  <p>主人公在图书馆中寻找相关的历史资料。</p>
  <h2 id="section2-3">2.3 重要发现</h2>
  <p>经过仔细研究，主人公发现了一个重要的历史秘密。</p>
</body>
</html>''',
        
        'OEBPS/chapter3.xhtml': '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>第三章：结束</title>
</head>
<body>
  <h1>第三章：结束</h1>
  <p>在最后一章中，所有的谜团都得到了解答，故事迎来了圆满的结局。</p>
  <p>主人公不仅完成了自己的研究，还为小镇的历史保护做出了重要贡献。</p>
  <h2 id="section3-1">3.1 真相大白</h2>
  <p>历史的真相终于浮出水面。</p>
  <h2 id="section3-2">3.2 成果展示</h2>
  <p>主人公将研究成果展示给了小镇的居民。</p>
  <h2 id="section3-3">3.3 新的开始</h2>
  <p>故事结束了，但这也是新冒险的开始。</p>
</body>
</html>'''
    }
    
    # 创建EPUB文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as epub:
        # 首先添加mimetype文件（不压缩）
        epub.writestr('mimetype', files['mimetype'], compress_type=zipfile.ZIP_STORED)
        
        # 添加其他文件
        for filename, content in files.items():
            if filename != 'mimetype':
                epub.writestr(filename, content)
    
    print(f"测试EPUB文件已创建: {output_path}")
    return output_path

if __name__ == '__main__':
    create_test_epub()