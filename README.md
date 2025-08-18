# Paul Graham Essay Crawler

This project provides a simple Python script to download Paul Graham's essays, save them as Markdown files, and bundle them into an EPUB ebook.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the crawler:
   ```bash
   python pg_crawler.py
   ```

Markdown copies of each essay will appear in the `articles/` directory, and the generated ebook will be `PaulGrahamEssays.epub`.

## Note

Some environments restrict access to `paulgraham.com`. If the script fails with a network error, you may need to run it from a different network or adjust proxy settings.
