import sys
import asyncio
from crawl import crawl_site_async



async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]

    print(f"Starting crawl of: {BASE_URL}...")
    page_data = await crawl_site_async(BASE_URL, 10)
    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links, {len(page['image_urls'])} image URLs")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
