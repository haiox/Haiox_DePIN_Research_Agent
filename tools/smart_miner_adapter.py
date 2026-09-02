from bs4 import BeautifulSoup
from core.llm_router import call_llm
from curl_cffi.requests import AsyncSession

async def fetch_raw_data_from_miner(target_url: str) -> str:
    """
    Extracts live data by bypassing Cloudflare and reliably resolves Windows encoding issues.
    """
    print(f"📡 [Adapter] Live Fetching & Bypassing Cloudflare for: {target_url}")
    
    try:
        # Use curl_cffi to fully impersonate a Chrome browser fingerprint and bypass Cloudflare
        async with AsyncSession(impersonate="chrome120", timeout=30.0) as session:
            response = await session.get(target_url)
            
        if response.status_code != 200:
            print(f"❌ [Adapter] Failed to fetch page. Status: {response.status_code}")
            return ""

        # Parse the HTML and remove extraneous sections that contain no useful data
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "noscript", "header", "aside"]):
            tag.extract()

        # Extract plain text
        raw_text = soup.get_text(separator=" ", strip=True)
        
        # ☢️ Final pass: remove all non-standard characters and emojis to prevent Windows crashes
        raw_text = raw_text.encode('ascii', errors='ignore').decode('ascii')
        
        clean_prompt = f"""
        Extract and summarize all core information about this Web3/DePIN project from the webpage text below.
        Include details on what the project does, its architecture, network bandwidth/hardware usage, token info, and claims.
        
        Raw Web Content:
        {raw_text[:12000]}
        """
        
        print("🧹 [Adapter] Cleaning and structuring raw text with GLM-5.3-Flash...")
        cleaned_content = await call_llm(clean_prompt, role="cheap")
        
        return cleaned_content

    except Exception as e:
        print(f"❌ [Adapter] Scraping/Extraction error: {e}")
        return ""
