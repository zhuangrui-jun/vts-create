## ADDED Requirements

### Requirement: LangGraph dialogue orchestration

The backend SHALL use LangGraph to define a state graph that processes each user message through context assembly, LLM generation, emotion extraction, and response formatting nodes.

#### Scenario: Complete dialogue flow

- **WHEN** a user sends a message to an existing conversation
- **THEN** the graph loads conversation history and assembles a context prompt, calls the LLM to generate a response, extracts an emotion label from the response, maps the emotion to a Live2D expression name, and returns both the text and expression name in the API response

#### Scenario: Empty conversation context

- **WHEN** a user sends the first message in a new conversation (no prior history)
- **THEN** the graph assembles context with only the system persona prompt and the current user message, and generates a response normally

### Requirement: Emotion extraction from LLM output

The LangGraph `emotion_extract` node SHALL analyze the LLM's response to classify the character's emotional state into one of the predefined categories: `happy`, `very_happy`, `embarrassed`, `sad`, or `neutral`.

#### Scenario: Happy emotion detected

- **WHEN** the LLM generates a response expressing joy, satisfaction, or amusement
- **THEN** the emotion_extract node outputs emotion `happy`

#### Scenario: Sad emotion detected

- **WHEN** the LLM generates a response expressing sorrow, disappointment, or sympathy
- **THEN** the emotion_extract node outputs emotion `sad`

#### Scenario: Invalid emotion fallback

- **WHEN** the emotion_extract node cannot confidently classify the response
- **THEN** it SHALL output emotion `neutral` as the default fallback

### Requirement: REST API for conversation management

The backend SHALL expose a REST API with the following endpoints for conversation CRUD and messaging.

#### Scenario: Create conversation

- **WHEN** a POST request is sent to `/api/conversations`
- **THEN** a new conversation record is created in SQLite with a generated title and the response returns the conversation object with status 201

#### Scenario: List conversations

- **WHEN** a GET request is sent to `/api/conversations`
- **THEN** the response returns all conversations ordered by most recent activity, each including id, title, and last_updated timestamp

#### Scenario: Get single conversation

- **WHEN** a GET request is sent to `/api/conversations/:id`
- **THEN** the response returns the conversation metadata and all its messages in chronological order

#### Scenario: Delete conversation

- **WHEN** a DELETE request is sent to `/api/conversations/:id`
- **THEN** the conversation and all its associated messages are removed from the database, and status 204 is returned

#### Scenario: Delete non-existent conversation

- **WHEN** a DELETE request is sent to `/api/conversations/:id` for an ID that does not exist
- **THEN** the response returns status 404 with an error message

#### Scenario: Send message

- **WHEN** a POST request with `{ "content": "user message" }` is sent to `/api/conversations/:id/messages`
- **THEN** the user message is persisted, the LangGraph pipeline processes it, and the response returns `{ "message": { ...user message }, "response": { "content": "...", "emotion": "...", "expression": "..." } }`

### Requirement: Character persona configuration

The backend SHALL support a configurable system prompt that defines the AI character's persona, loaded from an environment variable or config file.

#### Scenario: Custom persona prompt

- **WHEN** the backend starts with a configured persona prompt
- **THEN** all conversations use that persona as the system message in the LLM context
