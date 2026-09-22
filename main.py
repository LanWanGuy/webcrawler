import sys
from crawl import get_html, crawl_page



def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]

    print(f"Starting crawl of: {BASE_URL}...")
    page_data = crawl_page(BASE_URL)
    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links, {len(page['image_urls'])} image URLs")
    sys.exit(0)

if __name__ == "__main__":
    main()
