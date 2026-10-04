from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession


async def fetch_raw_data_from_miner(target_url: str) -> str:
    """Fetch visible page text without changing the source with an LLM."""
    try:
        async with AsyncSession(impersonate="chrome120", timeout=30.0) as session:
            response = await session.get(target_url)
        if response.status_code != 200:
            raise ValueError(f"HTTP {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        text = soup.get_text(separator=" ", strip=True)
        if not text:
            raise ValueError("Page has no visible text")
        return text[:30000]
    except Exception as exc:
        print(f"❌ [Adapter] Extraction failed: {exc}")
        return ""
