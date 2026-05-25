import httpx
from ..utils import get_relevant_images, extract_title


class Crawl4AIScraper:
    def __init__(self, link, session=None):
        self.link = link
        self.session = session
        self.base_url = "http://gptr-crawl4ai:11235"

    def scrape(self) -> tuple:
        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(
                    f"{self.base_url}/md",
                    json={"url": self.link, "fit": True},
                )
                resp.raise_for_status()
                data = resp.json()

            result = data.get("result", {})
            content = result.get("fit_markdown") or result.get("markdown", "")
            title = result.get("metadata", {}).get("title", "")

            image_urls = []
            for img in result.get("metadata", {}).get("images", [])[:10]:
                image_urls.append({"url": img.get("src", ""), "score": img.get("score", 0)})

            return content, image_urls, title

        except Exception as e:
            print(f"Crawl4AI error for {self.link}: {e}")
            return "", [], ""
