"""
web_loader.py - Web content loader for RAG system
"""

import asyncio
import requests
import certifi
from bs4 import BeautifulSoup
from langchain.schema import Document
from config import HTTP_TIMEOUT
from urllib.parse import urlparse

def validate_reference(url: str) -> tuple[bool, str]:
    """Validate a reference URL and return a snippet."""
    try:
        if not urlparse(url).scheme:
            return (False, "Invalid URL (no scheme)")
        
        resp = requests.head(url, allow_redirects=True, timeout=HTTP_TIMEOUT, verify=certifi.where())
        if 200 <= resp.status_code < 400:
            try:
                g = requests.get(url, stream=True, timeout=HTTP_TIMEOUT, verify=certifi.where())
                ctype = g.headers.get("Content-Type", "")
                snippet = ""
                if "text" in ctype or "html" in ctype or ctype == "":
                    snippet = g.text[:1500]
                else:
                    snippet = f"Content-Type: {ctype}"
                return (True, snippet)
            except Exception as e:
                return (True, f"Reachable (HEAD OK) but GET failed: {e}")
        else:
            return (False, f"HEAD returned status {resp.status_code}")
    except Exception as e:
        return (False, str(e))

class SimpleWebLoader:
    def __init__(self, urls):
        self.urls = urls
        
    async def aload(self):
        """Asynchronously load web content from URLs."""
        docs = []
        for url in self.urls:
            try:
                print(f"[DEBUG] Loading URL: {url}")
                response = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: requests.get(url, timeout=HTTP_TIMEOUT, verify=certifi.where())
                )
                soup = BeautifulSoup(response.text, 'html.parser')
                docs.append(Document(
                    page_content=soup.get_text(),
                    metadata={"source": url}
                ))
            except Exception as e:
                print(f"[DEBUG] Error loading {url}: {e}")
        return docs