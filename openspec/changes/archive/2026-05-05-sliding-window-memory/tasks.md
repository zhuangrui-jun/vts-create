## 1. Backend

- [x] 1.1 Extract `_tokenize()` into a shared utility in `backend/app/config/text_utils.py` (reusable by both sticker matching and memory retrieval)
- [x] 1.2 Implement `assemble_context()` in `backend/app/api/routes.py`: sliding window (last 5 rounds) + keyword retrieval (older messages matched via SQLite LIKE)
- [x] 1.3 Replace the current `history = [...]` line with `assemble_context()` call
- [x] 1.4 Verify: send messages in a conversation with > 5 rounds, confirm only last 5 rounds are in context, older matched messages appear when relevant
