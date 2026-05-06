## ADDED Requirements

### Requirement: Sliding window limits context to 5 rounds

The system SHALL include only the most recent 5 user-assistant message pairs in the LLM context, excluding older messages from the default context window.

#### Scenario: Conversation with more than 5 rounds

- **WHEN** a conversation has 10 rounds of history and the user sends a new message
- **THEN** only the last 5 rounds (10 messages) are included in the LLM context

#### Scenario: Conversation with 3 rounds

- **WHEN** a conversation has 3 rounds of history
- **THEN** all 3 rounds are included in the LLM context (no truncation needed)

### Requirement: Keyword retrieval for older messages

The system SHALL search messages beyond the sliding window for keyword matches against the current user input, and prepend matching messages to the context.

#### Scenario: Older message matches keyword

- **WHEN** the user says "你还记得我之前说的开心的事吗" and an older message beyond the 5-round window contains "开心"
- **THEN** that older message is prepended to the LLM context before the sliding window messages

#### Scenario: No keyword match in older messages

- **WHEN** the user's message has no keywords that match any older messages beyond the window
- **THEN** no older messages are added to the context (only sliding window is used)

### Requirement: Context assembly order

The assembled context SHALL follow the order: system prompt, matched older messages, sliding window messages.

#### Scenario: Context with retrieved messages

- **WHEN** older messages are retrieved via keyword matching
- **THEN** the context order is [system] → [matched old messages] → [last 5 rounds]
