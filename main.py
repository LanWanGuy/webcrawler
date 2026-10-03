import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report



async def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <base_url> <max_concurrency> <max_pages>")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]
    MAX_CONCURRENCY = int(sys.argv[2])
    MAX_PAGES = int(sys.argv[3])

    print(f"Starting crawl of: {BASE_URL}...")
    page_data = await crawl_site_async(BASE_URL, MAX_CONCURRENCY, MAX_PAGES)
    #print(f"Found {len(page_data)} pages:")
    #for page in page_data.values():
    #    print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links, {len(page['image_urls'])} image URLs")
    write_json_report(page_data)
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
