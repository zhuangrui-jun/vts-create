## Context

Bocha AI provides a fast (~150ms) search API at `https://api.bocha.cn/v1/ai-search` with Bearer auth. The LLM uses OpenAI's native tool calling with `stream=True` — when the model needs search it emits a `tool_calls` delta instead of content; when it doesn't, content streams immediately.

## Goals / Non-Goals

**Goals:**
- LLM autonomously decides when to invoke web search
- Search results injected as context for the LLM's response
- No text delay when search is not needed (streaming starts immediately)

**Non-Goals:**
- Direct display of search results to user (results are LLM context only)
- Multi-turn search refinement

## Decisions

### Streaming tool calling flow

```
User message → LLM call with tools=[web_search] + stream=True
  ├─ Model streams content immediately → no search needed (fast path)
  └─ Model emits tool_call delta → execute Bocha search → feed results back → continue streaming
```

The OpenAI streaming tool call API emits deltas with `delta.tool_calls` when the model wants to call a tool. We accumulate the tool call arguments, execute the search, then send a second message with the results.

### Bocha API integration

- Endpoint: `POST https://api.bocha.cn/v1/ai-search`
- Auth: `Authorization: Bearer <BOCHA_API_KEY>`
- Request: `{"query": "...", "freshness": "noLimit", "count": 5, "answer": false, "stream": false}`
- Response: web search results with title, url, snippet
- Results formatted as context: "搜索结果:\n1. [标题](URL)\n摘要\n..."

### Tool definition

```json
{
  "type": "function",
  "function": {
    "name": "web_search",
    "description": "搜索互联网获取实时信息。当需要最新新闻、天气、事件或不确定的信息时使用。",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {"type": "string", "description": "搜索关键词"}
      },
      "required": ["query"]
    }
  }
}
```

## Risks / Trade-offs

- Tool call path adds ~150ms (Bocha) + second LLM call overhead → Mitigation: acceptable for queries that genuinely need search
- LLM may over-trigger search → Mitigation: system prompt can guide restraint
