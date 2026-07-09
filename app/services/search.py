import os
from typing import Any
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
from ddgs import DDGS

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")


def _normalize_item(title: str | None, url: str | None, snippet: str | None, source: str) -> dict[str, Any]:
    return {
        "title": title or "",
        "url": url or "",
        "snippet": snippet or "",
        "source": source,
    }


def tavily_search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(
        query=query,
        max_results=max_results,
        include_answer=False,
        include_raw_content=False,
    )

    items = []
    for r in response.get("results", []):
        items.append(
            _normalize_item(
                title=r.get("title"),
                url=r.get("url"),
                snippet=r.get("content") or r.get("snippet"),
                source="tavily",
            )
        )
    return items


def brave_search(query: str, count: int = 5) -> list[dict[str, Any]]:
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {"q": query, "count": count}

    response = requests.get(url, headers=headers, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    items = []
    for r in data.get("web", {}).get("results", []):
        items.append(
            _normalize_item(
                title=r.get("title"),
                url=r.get("url"),
                snippet=r.get("description"),
                source="brave",
            )
        )
    return items


def duckduckgo_search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    items = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            items.append(
                _normalize_item(
                    title=r.get("title"),
                    url=r.get("href"),
                    snippet=r.get("body"),
                    source="duckduckgo",
                )
            )
    return items


def search_with_fallback(query: str) -> list[dict[str, Any]]:
    try:
        return tavily_search(query)
    except Exception as e:
        print(f"Tavily failed: {e}")

    try:
        return brave_search(query)
    except Exception as e:
        print(f"Brave failed: {e}")

    try:
        return duckduckgo_search(query)
    except Exception as e:
        print(f"DuckDuckGo failed: {e}")

    return []