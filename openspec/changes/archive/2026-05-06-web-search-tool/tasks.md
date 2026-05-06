## 1. Bocha API client

- [x] 1.1 Create `backend/app/config/web_search.py` with `search(query)` function: call Bocha API, parse results, return formatted text
- [x] 1.2 Add `BOCHA_API_KEY` to `.env`

## 2. Tool calling in LLM stream

- [x] 2.1 Define the `web_search` tool schema in `routes.py`
- [x] 2.2 Refactor the LLM streaming call in `generate()` to pass `tools` param and handle streaming tool calls
- [x] 2.3 Implement tool call accumulation: detect `delta.tool_calls`, accumulate function arguments, execute search when complete
- [x] 2.4 After search results return, send a second LLM request with results as context, stream response

## 3. Verify

- [x] 3.1 Test "你好" → no search, text streams immediately
- [x] 3.2 Test "今天有什么新闻" → tool called → search executed → response includes real-time info
