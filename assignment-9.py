
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def web_crawler(start_url, max_pages=10):
    visited = set()
    queue = deque([start_url])

    # Restrict crawling to the starting website
    domain = urlparse(start_url).netloc

    headers = {
        "User-Agent": "SimpleEducationalCrawler/1.0"
    }

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        try:
            response = requests.get(
                url, headers=headers, timeout=10
            )

            if response.status_code != 200:
                continue

            # Process HTML pages only
            content_type = response.headers.get(
                "Content-Type", ""
            )
            if "text/html" not in content_type.lower():
                continue

            visited.add(url)
            print("\nCrawled:", url)

            soup = BeautifulSoup(
                response.text, "html.parser"
            )

            title = soup.title.string.strip() if (
                soup.title and soup.title.string
            ) else "No title"

            print("Title:", title)

            # Extract hyperlinks
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(url, link["href"])
                parsed = urlparse(absolute_url)

                # Only follow HTTP/HTTPS links on same domain
                if (
                    parsed.scheme in ("http", "https")
                    and parsed.netloc == domain
                    and absolute_url not in visited
                    and absolute_url not in queue
                ):
                    queue.append(absolute_url)

        except requests.RequestException as error:
            print("Error crawling", url, ":", error)

    print("\nCrawling completed.")
    print("Total pages crawled:", len(visited))


if __name__ == "__main__":
    start_url = input(
        "Enter starting URL (e.g. https://example.com): "
    ).strip()

    web_crawler(start_url, max_pages=10)

