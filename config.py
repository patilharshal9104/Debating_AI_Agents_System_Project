"""
config.py - Configuration constants for the debate system
"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API configurations
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
DEEPSEEK_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek/deepseek-r1:free"

# Timeouts
HTTP_TIMEOUT = 12
LLM_TIMEOUT = 25

# High-authority domains for reference scoring
HIGH_AUTHORITY_DOMAINS = {
    "arxiv.org", "ieeexplore.ieee.org", "acm.org", "springer.com",
    "nature.com", "sciencedirect.com", "researchgate.net",
    "wikipedia.org", "github.com", "medium.com", "geeksforgeeks.org",
    "stackoverflow.com", "cplusplus.com", "pmindia.gov.in", "mea.gov.in",
    "indiabudget.gov.in", "prsindia.org", "worldbank.org"
}