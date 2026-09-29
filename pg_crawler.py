import os
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from ebooklib import epub
import markdown

BASE_URL = "http://www.paulgraham.com/"
INDEX_URL = BASE_URL + "articles.html"
ARTICLES_DIR = "articles"


def get_article_links():
    """Fetch the index page and extract article links."""
    resp = requests.get(INDEX_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Most article links look like 'foo.html'
        if re.match(r"^[\w-]+\.html$", href):
            links.append(BASE_URL + href)
    return links


def download_articles(links):
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    for url in links:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        slug = os.path.splitext(url.rsplit("/", 1)[-1])[0]
        markdown_content = md(resp.text)
        with open(os.path.join(ARTICLES_DIR, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Saved {slug}.md")


def build_epub():
    book = epub.EpubBook()
    book.set_identifier("pg-essays")
    book.set_title("Paul Graham Essays")
    book.set_language("en")

    chapters = []
    for fname in sorted(os.listdir(ARTICLES_DIR)):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(ARTICLES_DIR, fname), encoding="utf-8") as f:
            md_text = f.read()
        html = markdown.markdown(md_text)
        chapter = epub.EpubHtml(title=fname[:-3], file_name=fname[:-3] + ".xhtml", content=html)
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters

    epub.write_epub("PaulGrahamEssays.epub", book)
    print("Created PaulGrahamEssays.epub")


def main():
    links = get_article_links()
    download_articles(links)
    build_epub()


if __name__ == "__main__":
    main()
