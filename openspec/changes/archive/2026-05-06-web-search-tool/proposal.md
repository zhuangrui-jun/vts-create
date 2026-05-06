## Why

The AI character currently has no access to real-time information. When users ask about current events, weather, or recent news, the AI either makes things up or says it doesn't know. Adding a web search tool lets the AI fetch live data — and using the LLM's native tool calling means the model itself decides when search is needed, with minimal impact on response speed.

## What Changes

- New `web_search` tool powered by Bocha AI search API (`api.bocha.cn/v1/ai-search`)
- LLM uses OpenAI native tool calling to decide whether to invoke search
- Streaming flow: if no tool call needed, text streams immediately; if search is needed, results are fetched then text streams with enriched context
- New env vars: `BOCHA_API_KEY` for the search API
- Search results shown to the LLM as context, not directly to the user

## Capabilities

### New Capabilities

- `web-search-tool`: LLM-invoked Bocha AI search that fetches real-time web results and injects them into the conversation context

### Modified Capabilities

<!-- None -->

## Impact

- `backend/app/api/routes.py`: LLM call refactored to support tool calling + streaming
- `backend/app/config/web_search.py`: NEW — Bocha API client
- `.env`: New `BOCHA_API_KEY` variable
