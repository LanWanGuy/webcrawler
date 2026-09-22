from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit, urljoin
from typing import TypedDict
from requests.models import HTTPError
import sys,requests



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

def get_urls_from_html(html: str, base_url: str | None) -> list[str]:
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

def extract_page_data(html: str, page_url: str | None) -> PageData:
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

def get_html(url: str | None) -> str:
    try:
        try:
            response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
        except requests.exceptions.MissingSchema:
            response = requests.get(f"https://{url}", headers={"User-Agent": "BootCrawler/1.0"})
        if "text/html" not in response.headers.get("content-type",'').lower():
            raise Exception(f"unsupported content type: {response.headers['content-type']}")
        response.raise_for_status()
        return response.text
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"unexpected error occurred: {e}")
        sys.exit(1)

def crawl_page(base_url: str, current_url: str | None = None, page_data: dict[str, PageData] | None = None) -> dict[str, PageData] | None:
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
    if urlsplit(base_url).netloc != urlsplit(current_url).netloc:
        return page_data

    normalized_url = normalize_url(current_url)
    if normalized_url in page_data:
        return page_data
    print (f"Crawling: {current_url}...")
    html = get_html(current_url)
    page_data[normalized_url] = extract_page_data(html, current_url)
    for link in page_data[normalized_url]["outgoing_links"]:
        page_data = crawl_page(base_url, link, page_data)
    return page_data

def main():
    pass

if __name__ == "__main__":
    main()
