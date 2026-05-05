## Why

The current Live2D viewer renders a character model with manual expression controls but has no dialogue capability. Users want the character to converse naturally with AI-driven responses, and for the character's Live2D expressions to reflect the AI's emotional tone — creating a more immersive, lifelike interaction. Multi-conversation management with persistent history is essential for a chat-like experience.

## What Changes

- New **Python backend** using LangGraph to orchestrate AI dialogue flow, with a structured graph that determines the AI character's response text and emotional state from conversation context
- New **conversation API** (REST) supporting multi-conversation CRUD: create, list, switch, and delete conversation sessions
- **SQLite database** for persisting conversations, messages, and per-conversation metadata
- **Emotion-to-expression mapping** layer that translates the AI's inferred mood into the Live2D model's expression names (笑眯眯, 眯眯眼, 泪珠, 眼泪)
- New **frontend chat UI** component with conversation sidebar (multi-conversation list, delete button, new conversation) and message bubble area
- Integration of AI responses with the existing `live2dStore.setExpression()` to trigger expression changes in sync with dialogue

## Capabilities

### New Capabilities

- `chat-backend`: Python/LangGraph backend service that processes dialogue, infers character emotion, and returns text + expression commands; exposes REST API for conversation management
- `conversation-persistence`: SQLite schema and data access layer for conversations, messages, and expression history
- `chat-ui`: Frontend chat panel with multi-conversation sidebar, message display, input area, and delete-conversation functionality
- `emotion-expression-mapping`: Mapping from AI-detected emotional categories to Live2D model expression names, with configurable rules

### Modified Capabilities

<!-- No existing specs to modify -->

## Impact

- **Backend**: New Python service (`backend/`) with LangGraph, FastAPI (or similar), and SQLite dependencies
- **Frontend**: New Vue components in `src/components/chat/`, new store `chatStore.ts`, updates to `Live2DCanvas.vue` to accommodate chat panel layout
- **Dependencies**: Python packages (langgraph, fastapi, uvicorn, sqlite3 or sqlalchemy), frontend may need a fetch/axios wrapper for API calls
- **Live2D model**: Expression names must match the existing model's defined expressions; mapping layer should be configurable per character model
