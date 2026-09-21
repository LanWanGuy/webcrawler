from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    return urlsplit(url).netloc + urlsplit(url).path.removesuffix("/")


def get_heading_from_html(html: str) -> str:
    imput_html = BeautifulSoup(html, "html.parser")
    heading = imput_html.find("h1") or imput_html.find("h2")
    return heading.get_text(strip=True) if isinstance(heading, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    input_html = BeautifulSoup(html, "html.parser")
    main = input_html.find("main")
    if main.find_all("p"):
        paragraphs = main.find_all("p")
    else:
        paragraphs = input_html.find_all("p")
    return paragraphs[0].get_text(strip=True) if paragraphs else ""

def main():
    pass


if __name__ == "__main__":
    main()
