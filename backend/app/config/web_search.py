import os
import json
import logging
from urllib.request import Request, urlopen
from urllib.error import URLError

logger = logging.getLogger(__name__)

BOCHA_URL = "https://api.bocha.cn/v1/ai-search"


def search(query: str, count: int = 5) -> str:
    api_key = os.environ.get("BOCHA_API_KEY", "")
    if not api_key:
        logger.warning("BOCHA_API_KEY not set, search skipped")
        return "搜索功能未配置 (BOCHA_API_KEY)"

    body = json.dumps({
        "query": query,
        "freshness": "noLimit",
        "count": count,
        "answer": False,
        "stream": False,
    }).encode("utf-8")

    req = Request(BOCHA_URL, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        logger.error("Bocha search error: %s", e)
        return "搜索暂时不可用"
    except Exception as e:
        logger.error("Bocha search error: %s", e)
        return "搜索暂时不可用"

    # Parse new API response format: messages[].content (JSON string) contains value[]
    results = []
    for msg in data.get("messages", []):
        if msg.get("content_type") == "webpage":
            try:
                inner = json.loads(msg["content"])
                results.extend(inner.get("value", []))
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning("Failed to parse webpage content: %s", e)

    if not results:
        return f"未找到关于\"{query}\"的相关结果"

    lines = [f"搜索结果（{query}）："]
    for i, item in enumerate(results[:count], 1):
        title = item.get("name", "")
        url = item.get("url", "")
        snippet = item.get("snippet") or item.get("summary", "")
        date_pub = item.get("datePublished", "")
        date_str = f" ({date_pub})" if date_pub else ""
        lines.append(f"{i}. {title}{date_str}\n   {url}\n   {snippet}")

    return "\n".join(lines)
