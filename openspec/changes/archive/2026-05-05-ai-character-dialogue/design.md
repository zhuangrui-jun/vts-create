## Context

The project is a Live2D character viewer built with Vue 3 + TypeScript (frontend) and PixiJS for rendering. The current backend directory (`backend/app/`) is empty. The frontend already has a `live2dStore` with `setExpression()` for changing character expressions. This design adds an AI dialogue system where a Python/LangGraph backend drives both text responses and emotion-triggered expression changes on the Live2D model.

## Goals / Non-Goals

**Goals:**
- Python backend service with LangGraph orchestrating dialogue and emotion inference
- REST API for multi-conversation management (CRUD)
- SQLite persistence for conversations, messages, and metadata
- Frontend chat UI with conversation sidebar and message display
- Emotion-to-Live2D-expression mapping triggered by AI responses

**Non-Goals:**
- User authentication / multi-user support
- Streaming/SSE responses (initial version uses request-response)
- Voice/speech synthesis or audio input
- Model fine-tuning or custom LLM training
- Character personality customization UI (character persona is config-driven)

## Decisions

### 1. Backend: FastAPI + LangGraph

**Choice**: FastAPI for HTTP layer, LangGraph for dialogue orchestration.
**Why**: FastAPI is the standard async Python web framework with good ergonomics. LangGraph provides structured state machine semantics for the dialogue pipeline (context assembly → LLM → emotion extraction → response assembly). This separation makes each step testable in isolation.
**Alternatives**: Flask (less async-friendly), directly calling LLM without orchestration (harder to extend with memory, emotion, etc.).

### 2. LangGraph Graph Structure

The dialogue graph has these nodes:
```
[context_assembly] → [llm_generate] → [emotion_extract] → [response_format]
```
- `context_assembly`: Loads conversation history from DB, assembles system prompt with character persona
- `llm_generate`: Calls the LLM (OpenAI-compatible API) with assembled context to produce response text
- `emotion_extract`: Analyzes the LLM response text and conversation context to determine the character's emotional state
- `response_format`: Packages text + emotion + expression name into the API response

State flows through the graph as a typed dict containing messages, response text, emotion label, and the target expression name.

### 3. Database: SQLite with SQLAlchemy

**Choice**: SQLite via SQLAlchemy ORM.
**Why**: Zero-config, file-based, sufficient for single-user desktop app. SQLAlchemy provides clean migration support if we later move to PostgreSQL.
**Schema**:
- `conversations`: id, title, created_at, updated_at
- `messages`: id, conversation_id (FK), role (user/assistant), content, emotion, expression, created_at

### 4. Emotion-to-Expression Mapping

**Choice**: JSON config file mapping emotion categories to Live2D expression names.
**Why**: Each Live2D model may have different expression names. A config file makes it easy to adjust without code changes.
```json
{
  "happy": "笑眯眯",
  "very_happy": "眯眯眼",
  "embarrassed": "泪珠",
  "sad": "眼泪",
  "neutral": "normal"
}
```
The `emotion_extract` node outputs an emotion label, and the mapping layer resolves it to the model's expression name.

### 5. Frontend Architecture

**Choice**: New `chatStore` (Pinia) for conversation state, new `ChatPanel` component with `ConversationSidebar` and `MessageArea` sub-components.
**Why**: Keeps chat state separate from Live2D rendering state. The `chatStore` calls the backend API and, on receiving a response with an expression name, triggers `live2dStore.setExpression()`.

### 6. API Design

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/conversations | Create new conversation |
| GET | /api/conversations | List all conversations |
| GET | /api/conversations/:id | Get conversation with messages |
| DELETE | /api/conversations/:id | Delete conversation |
| POST | /api/conversations/:id/messages | Send message, get AI response |

## Risks / Trade-offs

- **LLM latency**: Each message round-trip is gated on LLM inference (1-5s). → Show typing indicator in UI; consider streaming via SSE in a future iteration.
- **Emotion accuracy**: LLM may produce inconsistent emotion labels. → Use a structured prompt with constrained emotion categories; the `emotion_extract` node can validate/fix labels against known set.
- **Expression name mismatch**: Live2D model must have the expressions mapped in config. → Validate at startup by checking available model expressions; log warnings if config references missing expressions.
- **SQLite concurrency**: Single-writer limitation. → Acceptable for single-user desktop app; use WAL mode for better read concurrency.

## Open Questions

- Which LLM provider/endpoint will be used? (Assume OpenAI-compatible API, configurable via environment variable)
- Should the character persona be a single fixed prompt or selectable? (Start with single configurable persona prompt)
