"""
utils.py - Utility functions for the debate system
"""

import time
import json
import re
import tldextract
from urllib.parse import urlparse
from config import HIGH_AUTHORITY_DOMAINS

def domain_from_url(url: str) -> str:
    """Extract domain from a URL."""
    try:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}".lower()
        return ext.domain.lower() if ext.domain else ""
    except Exception:
        return ""

def safe_json_parse(s: str, stage: str = "unknown") -> dict | None:
    """Safely parse JSON string, return None on failure."""
    try:
        # Look for a complete JSON object
        json_match = re.search(r'\{[\s\S]*\}', s)
        if not json_match:
            print(f"[DEBUG] No JSON block found in {stage} response: {s[:100]}...")
            return None
        json_str = json_match.group(0)
        parsed = json.loads(json_str)
        if not isinstance(parsed, dict):
            print(f"[DEBUG] Parsed {stage} response is not a dict: {json_str[:100]}...")
            return None
        # Validate required keys based on stage
        required_keys = {"answer"} if stage in ["initial_suggestion", "refinement"] else {"critique"} if stage == "critique" else {"final_answer"}
        if not required_keys.issubset(parsed.keys()):
            print(f"[DEBUG] Missing required keys in {stage} JSON: {json_str[:100]}...")
            return None
        return parsed
    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON decode error in {stage} response: {e}, input: {s[:100]}...")
        return None
    except Exception as e:
        print(f"[DEBUG] Unexpected error parsing JSON in {stage}: {e}, input: {s[:100]}...")
        return None

def now_ts() -> float:
    """Return current timestamp."""
    return time.time()

def calculate_authority_score(domain: str) -> int:
    """Calculate authority score for a domain."""
    if domain in HIGH_AUTHORITY_DOMAINS:
        return 3
    elif any(auth_domain in domain for auth_domain in HIGH_AUTHORITY_DOMAINS):
        return 2
    return 1