## ADDED Requirements

### Requirement: SQLite database initialization

The backend SHALL automatically create the SQLite database and tables on first startup if they do not exist.

#### Scenario: First startup creates database

- **WHEN** the backend starts and no SQLite database file exists
- **THEN** the database file is created with the `conversations` and `messages` tables using the correct schema

#### Scenario: Subsequent startup preserves data

- **WHEN** the backend starts and the SQLite database file already exists
- **THEN** no schema changes are applied and all existing data is preserved

### Requirement: Conversations table

The database SHALL have a `conversations` table with columns: `id` (TEXT PRIMARY KEY, UUID), `title` (TEXT NOT NULL), `created_at` (DATETIME NOT NULL), `updated_at` (DATETIME NOT NULL).

#### Scenario: Create conversation record

- **WHEN** a new conversation is created via the API
- **THEN** a row is inserted with a generated UUID, an initial title derived from the first message or a default value, and timestamps set to the current time

#### Scenario: Update conversation timestamp

- **WHEN** a new message is added to a conversation
- **THEN** the conversation's `updated_at` field is set to the current time

### Requirement: Messages table

The database SHALL have a `messages` table with columns: `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `conversation_id` (TEXT NOT NULL, FK references conversations.id ON DELETE CASCADE), `role` (TEXT NOT NULL, CHECK role IN ('user', 'assistant')), `content` (TEXT NOT NULL), `emotion` (TEXT), `expression` (TEXT), `created_at` (DATETIME NOT NULL).

#### Scenario: Insert user message

- **WHEN** a user sends a message to a conversation
- **THEN** a row is inserted with role `user`, content set to the message text, and emotion/expression set to NULL

#### Scenario: Insert assistant message with emotion

- **WHEN** the AI generates a response with an emotion and expression
- **THEN** a row is inserted with role `assistant`, content set to the response text, and emotion/expression set to the extracted values

#### Scenario: Cascade delete messages

- **WHEN** a conversation is deleted
- **THEN** all messages belonging to that conversation are automatically deleted via the foreign key cascade

### Requirement: Conversation title generation

The system SHALL auto-generate a conversation title from the first user message, truncating to a maximum of 50 characters.

#### Scenario: Title from first message

- **WHEN** the first message in a conversation is "你好，今天天气怎么样？"
- **THEN** the conversation title is set to "你好，今天天气怎么样？" (or truncated if > 50 chars)

#### Scenario: Default title fallback

- **WHEN** a conversation is created without an initial message
- **THEN** the conversation title is set to "新对话"
