## Context

Current context assembly loads ALL conversation messages into the LLM context. This unbounded growth causes token bloat and eventual context window overflow.

## Goals / Non-Goals

**Goals:**
- Always include the last 5 rounds (10 messages) in LLM context
- Retrieve relevant older messages via keyword matching against current user input
- Keep the implementation simple — SQLite LIKE-based keyword search, no embeddings

**Non-Goals:**
- Embedding-based semantic search
- Summarization of old messages
- Configurable window size via UI (hardcoded to 5 for now)

## Decisions

### 1. Sliding window: 5 rounds

Always take the last 5 user + 5 assistant messages. For conversations with ≤ 5 rounds, this is equivalent to the current behavior.

### 2. Keyword retrieval for older messages

For messages beyond the 5-round window:
- Extract 2-4 char substrings from the current user message (reuse `_tokenize` approach from sticker matching)
- Search older messages: `WHERE content LIKE '%token%'` for each token
- Collect unique matching messages, ordered by original timestamp
- Prepend them to the sliding window as additional context

### 3. Context assembly order

```
[system prompt]
[matched older messages (if any)]
[last 5 rounds = up to 10 messages]
[current user message]
```

## Risks / Trade-offs

- Simple keyword matching may miss semantically relevant messages → Mitigation: acceptable trade-off for simplicity; can upgrade to embeddings later
- No deduplication between retrieved and window messages → Mitigation: filter by message ID to avoid duplicates
