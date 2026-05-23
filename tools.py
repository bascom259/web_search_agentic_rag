from ddgs import DDGS
import requests
from bs4 import BeautifulSoup


def search_web(query, max_results=5):

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        return [r["href"] for r in results]

    except:
        return []


def scrape_page(url):

    try:
        res = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        return text.strip()[:1500]

    except:
        return ""


def chunk_text(text, size=300):

    words = text.split()

    return [
        " ".join(words[i:i+size])
        for i in range(0, len(words), size)
    ]