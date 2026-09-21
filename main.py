import sys, requests
from requests.models import HTTPError

def get_html(url: str) -> str:
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

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]
    #page_data = extract_page_data(url)
    print(f"starting crawl of: {BASE_URL}")
    response = get_html(BASE_URL)
    print(response)

if __name__ == "__main__":
    main()
