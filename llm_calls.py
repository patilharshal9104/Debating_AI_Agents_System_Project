"""
llm_calls.py - Functions for calling Gemini and DeepSeek APIs
"""

import asyncio
import aiohttp
import requests
import certifi
import re
import json
from typing import Tuple, List
from config import GEMINI_URL, DEEPSEEK_URL, DEEPSEEK_MODEL, LLM_TIMEOUT, DEEPSEEK_API_KEY
from utils import safe_json_parse, urlparse

async def call_gemini_async(prompt: str) -> Tuple[str, List[str]]:
    print("[DEBUG] Calling Gemini API")
    system_prompt = (
        "You are Gemini 2.0 Flash, a panelist in a news channel debate. Provide a concise, technical, and factual answer (max 500 words). "
        "End with a JSON block with keys: 'answer' (string) and 'references' (list of 3-5 valid HTTPS URLs to official or reputable sources). "
        "Example: {\"answer\": \"...\", \"references\": [\"https://www.pmindia.gov.in\", \"https://www.mea.gov.in\"]}"
    )

    combined = system_prompt + "\n\nQUESTION:\n" + prompt

    payload = {
        "contents": [{"parts": [{"text": combined}]}],
        "generationConfig": {"temperature": 0.2, "topP": 0.9, "maxOutputTokens": 2048}
    }

    headers = {"Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GEMINI_URL, headers=headers, json=payload, timeout=LLM_TIMEOUT) as resp:
                text = await resp.text()
                if resp.status != 200:
                    print(f"[DEBUG] Gemini HTTP error: {resp.status}")
                    return (f"[Gemini HTTP {resp.status}] {text[:800]}", [])
                
                json_block = safe_json_parse(text, "gemini_response")
                if not json_block:
                    print(f"[DEBUG] Gemini malformed response: {text[:100]}...")
                    urls = re.findall(r"https?://[^\s)]+", text)
                    return (text.strip(), urls)

                textual = ""
                if "candidates" in json_block and len(json_block["candidates"]) > 0:
                    cand = json_block["candidates"][0].get("content", {})
                    if isinstance(cand, dict) and "parts" in cand:
                        textual = " ".join(p.get("text", "") for p in cand["parts"] if isinstance(p, dict))
                    elif "text" in cand:
                        textual = cand["text"]
                    else:
                        textual = json.dumps(cand)
                else:
                    textual = text

                inner_json = safe_json_parse(textual, "gemini")
                if inner_json:
                    answer = inner_json.get("answer", "") or inner_json.get("final_answer", "")
                    refs = inner_json.get("references", []) or []
                    refs = [str(r).strip() for r in refs if r and isinstance(r, str) and urlparse(r).scheme in ["http", "https"]]
                    print(f"[DEBUG] Gemini response parsed: {len(answer)} chars, {len(refs)} refs")
                    return (answer.strip() or textual.strip(), refs)
                else:
                    urls = re.findall(r"https?://[^\s)]+", textual)
                    print(f"[DEBUG] Gemini fallback to regex: {len(urls)} URLs")
                    return (textual.strip(), urls)
    except asyncio.TimeoutError:
        print("[DEBUG] Gemini timeout")
        return ("[Gemini Timeout]", [])
    except Exception as e:
        print(f"[DEBUG] Gemini exception: {e}")
        return (f"[Gemini Exception] {e}", [])

async def call_deepseek_async(prompt: str) -> Tuple[str, List[str]]:
    print("[DEBUG] Calling DeepSeek API")
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: call_deepseek_sync(prompt))

def call_deepseek_sync(prompt: str) -> Tuple[str, List[str]]:
    system_note = (
        "You are DeepSeek, a panelist in a news channel debate. Provide a concise, technical, and factual answer (max 500 words). "
        "End with a JSON object with keys: 'answer' (string) and 'references' (list of 3-5 valid HTTPS URLs to official or reputable sources). "
        "Example: {\"answer\": \"...\", \"references\": [\"https://www.pmindia.gov.in\", \"https://www.mea.gov.in\"]}"
    )
    full_prompt = system_note + "\n\nQUESTION:\n" + prompt

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Advanced Debate Agent"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=LLM_TIMEOUT, verify=certifi.where())
        text = resp.text
        if resp.status_code != 200:
            print(f"[DEBUG] DeepSeek HTTP error: {resp.status_code}")
            return (f"[DeepSeek HTTP {resp.status_code}] {text[:800]}", [])
        
        data = safe_json_parse(text, "deepseek_response")
        if not data:
            print(f"[DEBUG] DeepSeek malformed response: {text[:100]}...")
            urls = re.findall(r"https?://[^\s)]+", text)
            return (text.strip(), urls)

        textual = ""
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            msg = choice.get("message") or choice.get("text") or {}
            if isinstance(msg, dict):
                textual = msg.get("content", "") or msg.get("text", "")
            else:
                textual = str(msg)
            if not textual:
                textual = json.dumps(choice)
        else:
            textual = text

        inner_json = safe_json_parse(textual, "deepseek")
        if inner_json:
            answer = inner_json.get("answer", "") or inner_json.get("final_answer", "")
            refs = inner_json.get("references", []) or []
            refs = [str(r).strip() for r in refs if r and isinstance(r, str) and urlparse(r).scheme in ["http", "https"]]
            print(f"[DEBUG] DeepSeek response parsed: {len(answer)} chars, {len(refs)} refs")
            return (answer.strip() or textual.strip(), refs)
        else:
            urls = re.findall(r"https?://[^\s)]+", textual)
            print(f"[DEBUG] DeepSeek fallback to regex: {len(urls)} URLs")
            return (textual.strip(), urls)
    except requests.Timeout:
        print("[DEBUG] DeepSeek timeout")
        return ("[DeepSeek Timeout]", [])
    except Exception as e:
        print(f"[DEBUG] DeepSeek exception: {e}")
        return (f"[DeepSeek Exception] {e}", [])