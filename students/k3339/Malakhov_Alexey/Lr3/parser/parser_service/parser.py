import aiohttp
from bs4 import BeautifulSoup


def extract_title_description(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    for sup in soup.find_all("sup"):
        sup.decompose()

    heading = soup.find("h1", id="firstHeading")
    title = heading.get_text(strip=True) if heading else "Unknown"

    description = ""
    for p in soup.select("#mw-content-text .mw-parser-output > p"):
        text = p.get_text(strip=True)
        if len(text) > 80:
            description = text[:500]
            break

    return title, description or "No description available."


async def fetch_and_parse(url: str) -> tuple[str, str]:
    async with aiohttp.ClientSession() as http:
        async with http.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            resp.raise_for_status()
            html = await resp.text()
    return extract_title_description(html)
