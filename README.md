# EPUB to Markdown Converter

This tool converts EPUB files to Markdown, saving each chapter as a separate `.md` file and preserving images.

## Features

- Converts EPUB chapters to individual Markdown files.
- Extracts images from the EPUB and saves them locally.
- Attempts to preserve basic formatting.
- Allows user to specify input EPUB file and output directory name.

## Prerequisites

- Python 3.x
- brew install --cask wkhtmltopdf
- PDF转换功能依赖于 wkhtmltopdf 。请确保您已在系统中安装了 wkhtmltopdf 并将其添加到了系统PATH中。您可以从 wkhtmltopdf官网 下载。
- 如果选择输出PDF，脚本仍会像以前一样处理和保存图片到 images 文件夹，但主要的输出将是单个PDF文件。

## Installation

1.  **Clone the repository or download the files.**

2.  **Navigate to the project directory:**
    ```bash
    cd path/to/epub2md_en
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the script from your terminal:**
    ```bash
    python epub_to_markdown.py
    ```

2.  **Enter the path to your EPUB file** when prompted.
    Example: `/path/to/your/book.epub`

3.  **Enter a name for the output folder** where the Markdown files and images will be saved.
    Example: `my_converted_book`

    The script will create this folder if it doesn't exist and place the converted Markdown files (one per chapter) and an `images` subfolder within it.

## How it Works

-   The script uses the `ebooklib` library to parse the EPUB file.
-   It iterates through each document item (typically chapters) in the EPUB.
-   For each chapter:
    -   It uses `BeautifulSoup` to parse the HTML content.
    -   Images (`<img>` tags) are identified. The script attempts to find these images within the EPUB's items, saves them to an `images` folder in the output directory, and updates the image `src` attributes in the HTML to point to the local copies.
    -   The modified HTML content is then converted to Markdown using the `html2text` library.
    -   A filename for the Markdown file is generated using the chapter number and, if available, a title extracted from heading tags (`<h1>`, `<h2>`, etc.) or the `<title>` tag.
    -   The Markdown content is saved to a `.md` file.

## Limitations

-   Complex layouts and styling might not be perfectly preserved, as Markdown has a simpler structure than HTML/CSS.
-   The script's ability to find chapter titles depends on the EPUB's structure (presence of `<h1>`, `<h2>`, `<title>` tags).
-   Image path resolution might not cover all edge cases in EPUB structures, though common relative paths like `../images/` are handled.

## Contributing

Feel free to fork the project and submit pull requests.

## License

This project is open source and available under the MIT License.