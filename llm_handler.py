# llm_handler.py
import os
import requests

# Gemini API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://api.generative.google/v1beta2/models/text-bison-001:generate"

def flatten_for_prompt(kb_dict, prefix=""):
    """
    Recursively flatten KB dictionary into a list of lines for prompt.
    Fixes UnboundLocalError when 'v' is not a dict/list/string.
    """
    lines = []
    if isinstance(kb_dict, dict):
        for k, v in kb_dict.items():
            lines += flatten_for_prompt(v, f"{prefix}{k}.")
    elif isinstance(kb_dict, list):
        for i, v in enumerate(kb_dict):
            lines += flatten_for_prompt(v, f"{prefix}{i}.")
    elif kb_dict is not None:
        lines.append(f"{prefix[:-1]}: {kb_dict}")
    return lines

def generate_llm_response(query, kb_data=None):
    """
    Generate response using Gemini API.
    Falls back to KB if Gemini fails.
    """
    # Flatten KB
    kb_lines = flatten_for_prompt(kb_data.get("kb_dict", {})) if kb_data else []
    prompt_text = "\n".join(kb_lines) + "\n\nUser Query: " + query

    # Gemini API request
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt_text,
        "temperature": 0.7,
        "max_output_tokens": 512
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0].get("content", "Sorry, I could not generate an answer.")
        else:
            # Fallback
            return fallback_kb_response(query, kb_lines)
    except Exception as e:
        print(f"[LLM ERROR] Gemini API failed: {e}")
        # Fallback to KB only
        return fallback_kb_response(query, kb_lines)

def fallback_kb_response(query, kb_lines):
    """
    Simple KB-based fallback if LLM fails.
    Returns best match line or generic message.
    """
    query_lower = query.lower()
    matches = [line for line in kb_lines if query_lower in line.lower()]
    if matches:
        return matches[0]
    else:
        return "Sorry, I could not find an answer in the knowledge base."
