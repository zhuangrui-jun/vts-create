## 1. Backend project setup

- [x] 1.1 Create Python project structure under `backend/` with `requirements.txt`, `app/main.py`, `app/db/`, `app/graph/`, `app/api/`, `app/config/`
- [x] 1.2 Add Python dependencies: `langgraph`, `fastapi`, `uvicorn`, `sqlalchemy`, `openai`, `python-dotenv`, `pydantic`
- [x] 1.3 Create `.env` file with configurable variables: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `CHARACTER_PERSONA`, `EMOTION_MAPPING_PATH`

## 2. Database layer

- [x] 2.1 Create SQLAlchemy engine and session factory in `app/db/database.py` with SQLite WAL mode
- [x] 2.2 Define `Conversation` and `Message` ORM models in `app/db/models.py`
- [x] 2.3 Implement database auto-initialization on startup (create tables if not exist)

## 3. Emotion mapping

- [x] 3.1 Create default `emotion_mapping.json` config file with the five emotion-to-expression mappings
- [x] 3.2 Implement `app/config/emotion_mapping.py` to load and query the mapping, with case-insensitive normalization and `neutral` fallback for unknown emotions
- [x] 3.3 Add startup validation that logs warnings for expression names not in the model's available list

## 4. LangGraph dialogue pipeline

- [x] 4.1 Define the state type (`GraphState`) with fields: messages, response_text, emotion, expression
- [x] 4.2 Implement `context_assembly` node: load conversation history from DB, prepend character persona system prompt
- [x] 4.3 Implement `llm_generate` node: call OpenAI-compatible API with assembled context
- [x] 4.4 Implement `emotion_extract` node: analyze LLM response text to classify emotion into predefined categories
- [x] 4.5 Implement `response_format` node: resolve emotion to expression name and package final output
- [x] 4.6 Build and compile the LangGraph state graph in `app/graph/graph.py`

## 5. REST API

- [x] 5.1 Create Pydantic schemas for request/response models in `app/api/schemas.py`
- [x] 5.2 Implement `POST /api/conversations` endpoint (create conversation)
- [x] 5.3 Implement `GET /api/conversations` endpoint (list all conversations, ordered by most recent)
- [x] 5.4 Implement `GET /api/conversations/{id}` endpoint (get single conversation with messages)
- [x] 5.5 Implement `DELETE /api/conversations/{id}` endpoint (delete conversation and messages)
- [x] 5.6 Implement `POST /api/conversations/{id}/messages` endpoint (send message, run LangGraph, return AI response with expression)
- [x] 5.7 Add CORS middleware for frontend dev server access
- [x] 5.8 Create FastAPI app entry point in `app/main.py` with lifespan for DB init

## 6. Frontend chat infrastructure

- [x] 6.1 Create `chatStore.ts` Pinia store with state: conversations list, active conversation, messages, loading state
- [x] 6.2 Implement API client utilities in `src/composables/useChatApi.ts` for all conversation endpoints
- [x] 6.3 Add chat store actions: createConversation, loadConversations, selectConversation, deleteConversation, sendMessage
- [x] 6.4 Wire `chatStore.sendMessage` to call `live2dStore.setExpression()` when AI response includes an expression name

## 7. Frontend chat UI

- [x] 7.1 Create `ChatPanel.vue` container component with sidebar + message area layout
- [x] 7.2 Create `ConversationSidebar.vue` with conversation list, "新对话" button, and per-item delete button with confirmation dialog
- [x] 7.3 Create `MessageArea.vue` with chronological message list, user/assistant message styling, auto-scroll to bottom
- [x] 7.4 Create `MessageInput.vue` with text input, send button, Enter-to-send, empty-message guard
- [x] 7.5 Create `TypingIndicator.vue` (animated dots) shown while waiting for AI response
- [x] 7.6 Integrate `ChatPanel` into `Live2DCanvas.vue` layout (side-by-side or overlay depending on viewport)

## 8. Integration and polish

- [x] 8.1 Add loading and error states to all UI components (API errors, empty conversations, network errors)
- [x] 8.2 Test end-to-end flow: create conversation → send message → receive response + expression change → switch conversation → delete conversation
- [x] 8.3 Ensure responsive layout works at mobile (< 768px), tablet, and desktop widths
