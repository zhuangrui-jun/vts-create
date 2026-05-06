## Why

Currently every message loads the full conversation history into the LLM context window. As conversations grow, token costs increase and responses degrade when context exceeds the model's effective range. A sliding window + retrieval system keeps context bounded while preserving access to relevant older information.

## What Changes

- **Sliding window**: Only the last 5 rounds (5 user + 5 assistant messages) are always included in the LLM context
- **SQLite keyword retrieval**: Older messages beyond the window are searched via keyword matching against the current user input; matching messages are prepended as additional context
- Context assembly logic in `routes.py` is refactored to apply the sliding window + retrieval instead of loading all history

## Capabilities

### New Capabilities

- `sliding-window-context`: Limits LLM context to last 5 rounds + keyword-matched older messages from SQLite

### Modified Capabilities

<!-- No existing specs to modify -->

## Impact

- `backend/app/api/routes.py`: Context assembly section (lines 160-166) refactored to implement sliding window + retrieval
- `backend/app/config/sticker_index.py`: May reuse the `_tokenize()` utility for keyword extraction
