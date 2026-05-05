## ADDED Requirements

### Requirement: Chat panel layout

The frontend SHALL display a chat panel alongside the existing Live2D canvas, with a conversation sidebar on the left and a message area on the right.

#### Scenario: Chat panel renders

- **WHEN** the application loads with the Live2D model ready
- **THEN** a chat panel is visible containing an empty conversation sidebar and a message area with a prompt to start a conversation

#### Scenario: Responsive layout

- **WHEN** the viewport width is below 768px
- **THEN** the chat panel SHALL overlay or stack below the Live2D canvas rather than sit side-by-side

### Requirement: Conversation sidebar

The sidebar SHALL list all conversations with their titles, support creating new conversations, and allow deleting existing ones.

#### Scenario: List conversations

- **WHEN** the backend has existing conversations
- **THEN** the sidebar displays each conversation's title and last-updated time, sorted by most recent activity

#### Scenario: Create new conversation

- **WHEN** the user clicks a "新对话" (New Conversation) button in the sidebar
- **THEN** a new conversation is created via the API and appears at the top of the conversation list

#### Scenario: Switch conversation

- **WHEN** the user clicks on a conversation in the sidebar
- **THEN** the message area loads and displays that conversation's full message history

#### Scenario: Delete conversation with confirmation

- **WHEN** the user clicks the delete button on a conversation and confirms the action
- **THEN** the conversation is deleted via the API and removed from the sidebar list; if the deleted conversation was the active one, the message area clears

#### Scenario: Empty state

- **WHEN** no conversations exist
- **THEN** the sidebar shows an empty state message "暂无对话，点击上方按钮开始"

### Requirement: Message display

The message area SHALL display messages in chronological order, distinguishing user messages from AI character messages with visual differences (alignment, avatar, color).

#### Scenario: Display message history

- **WHEN** the user opens a conversation with prior messages
- **THEN** all messages are displayed in chronological order, with user messages right-aligned and AI messages left-aligned

#### Scenario: Display new AI response

- **WHEN** the backend returns an AI response with text and expression name
- **THEN** the AI message appears in the message area with its text content, and the Live2D character's expression changes to the returned expression name

#### Scenario: Typing indicator

- **WHEN** the user sends a message and is waiting for the AI response
- **THEN** a typing indicator (animated dots) is shown in the message area until the response arrives

### Requirement: Message input

The frontend SHALL provide a text input area at the bottom of the message panel for composing and sending messages.

#### Scenario: Send message with Enter

- **WHEN** the user types a message and presses Enter
- **THEN** the message is sent to the backend API, the input clears, and the message appears in the message area with a pending/sent state

#### Scenario: Send message with button

- **WHEN** the user types a message and clicks the send button
- **THEN** the message is sent to the backend API and the input clears

#### Scenario: Prevent empty message

- **WHEN** the user presses Enter or clicks send with an empty input
- **THEN** no message is sent

### Requirement: Expression trigger on AI response

When an AI response includes an expression name, the chat store SHALL trigger the Live2D expression change via `live2dStore.setExpression()`.

#### Scenario: Expression changes on happy response

- **WHEN** the AI response returns `{ "expression": "笑眯眯" }`
- **THEN** `live2dStore.setExpression("笑眯眯")` is called, and the Live2D model displays the 笑眯眯 expression

#### Scenario: Expression changes on sad response

- **WHEN** the AI response returns `{ "expression": "眼泪" }`
- **THEN** `live2dStore.setExpression("眼泪")` is called, and the Live2D model displays the 眼泪 expression
