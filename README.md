# EPUB to Any Format Converter

A Python tool to convert EPUB files to various formats including Markdown, HTML, and PDF with advanced navigation features.

## Features

- Convert EPUB to Markdown with proper formatting
- Extract and preserve images from EPUB files
- Generate HTML output with embedded CSS
- **🆕 Create PDF files with interactive table of contents and bookmarks**
- **🆕 Support chapter navigation and jumping in PDF**
- **🆕 Automatic page numbering in PDF output**
- Handle internal links and references
- Sanitize filenames for cross-platform compatibility

## Requirements

- Python 3.6+
- Required packages (install via `pip install -r requirements.txt`):
  - ebooklib
  - beautifulsoup4
  - html2text
  - pyppeteer
  - xhtml2pdf
  - **🆕 PyPDF2** (for PDF bookmarks and navigation)

## Installation

1. Clone this repository:
```bash
git clone git@github.com:Garfier/epub2any.git
cd epub2any
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python epub_to_markdown.py <epub_file> <output_directory> [--format FORMAT]
```

### Parameters

- `epub_file`: Path to the input EPUB file
- `output_directory`: Directory where converted files will be saved
- `--format`: Output format (markdown, html, pdf) - default is 'markdown'

### Examples

1. Convert to Markdown (default):
```bash
python epub_to_markdown.py book.epub output/
```

2. Convert to HTML:
```bash
python epub_to_markdown.py book.epub output/ --format html
```

3. **Convert to PDF with navigation** (🆕 Enhanced):
```bash
python epub_to_markdown.py book.epub output/ --format pdf
```

4. **Test PDF navigation features**:
```bash
python test_pdf_navigation.py book.epub output_test/
```

## Output Structure

### Markdown Output
- Individual `.md` files for each chapter
- `images/` directory containing extracted images
- Preserved internal links between chapters

### HTML Output
- Single HTML file with embedded CSS
- Inline images (base64 encoded)
- Styled for readability

### PDF Output (🆕 Enhanced)
- Single PDF file with all content
- **📖 Interactive table of contents at the beginning**
- **🔗 Clickable chapter links for easy navigation**
- **📑 PDF bookmarks/outline for quick jumping**
- **📄 Page numbers in header/footer**
- Preserved formatting and images
- Optimized typography and layout

## 🆕 New PDF Navigation Features

### Table of Contents
- Automatically generated from EPUB chapter structure
- Clickable links to jump to specific chapters
- Clean, professional formatting

### PDF Bookmarks
- Browser-style navigation panel
- Hierarchical chapter structure
- One-click jumping to any section

### Page Numbering
- Consistent page numbers throughout the document
- Header/footer with navigation information

### Internal Links
- All cross-references remain functional
- Smooth navigation between related sections

## Features in Detail

### Image Handling
- Extracts images from EPUB files
- Converts images to web-compatible formats
- Updates image references in converted content

### Link Processing
- Preserves internal links between chapters
- Updates link references for the target format
- Maintains document structure and navigation
- **🆕 Enhanced PDF internal linking with unique IDs**

### Filename Sanitization
- Removes or replaces invalid characters
- Ensures cross-platform compatibility
- Preserves meaningful filenames

## Testing

Use the included test script to verify PDF navigation features:

```bash
python test_pdf_navigation.py your_book.epub test_output/
```

This will demonstrate:
- Table of contents generation
- Bookmark creation
- Internal link functionality
- Page numbering

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Make sure all required packages are installed
2. **Permission errors**: Ensure write permissions for the output directory
3. **Large files**: PDF conversion may take time for large EPUB files
4. **🆕 PyPDF2 not found**: Install with `pip install PyPDF2` for bookmark features

### Error Messages

- "No items found in EPUB": The EPUB file may be corrupted or empty
- "Failed to extract images": Check if the EPUB contains valid image files
- "PDF generation failed": Ensure pyppeteer is properly installed
- **🆕 "PyPDF2 not available"**: Bookmarks will be skipped, but PDF will still be generated

## Performance Notes

- PDF generation with navigation features may take longer for large books
- Bookmark creation adds minimal overhead
- Table of contents generation is automatic and fast

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.