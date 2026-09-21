from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit, urljoin
from typing import TypedDict



class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    return urlsplit(url).netloc + urlsplit(url).path.removesuffix("/")


def get_heading_from_html(html: str) -> str:
    imput_html = BeautifulSoup(html, "html.parser")
    heading = imput_html.find("h1") or imput_html.find("h2")
    return heading.get_text(strip=True) if isinstance(heading, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    input_html = BeautifulSoup(html, "html.parser")
    main = input_html.find("main")
    if main and main.find_all("p"):
        paragraphs = main.find_all("p")
    else:
        paragraphs = input_html.find_all("p")
    return paragraphs[0].get_text(strip=True) if paragraphs else ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    input_html = BeautifulSoup(html, "html.parser")
    urls = []
    for anchor in input_html.find_all("a"):
        href = anchor.get("href")
        if href and urlsplit(href).netloc:
            urls.append(href)
        elif href:
            urls.append(urljoin(base_url,href))
    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    input_html = BeautifulSoup(html, "html.parser")
    images = []
    for img in input_html.find_all("img"):
        src = img.get("src")
        if src and urlsplit(src).netloc:
            images.append(src)
        elif src:
            images.append(urljoin(base_url, src))
    return images

def extract_page_data(html: str, page_url: str) -> PageData:
    #url = normalize_url(page_url)
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)
    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls
    }


def main():
    pass

if __name__ == "__main__":
    main()
