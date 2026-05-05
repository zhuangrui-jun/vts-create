export interface ConversationListItemData {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface MessageData {
  id: number
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  emotion: string | null
  expression: string | null
  created_at: string
}

export interface ConversationData {
  id: string
  title: string
  created_at: string
  updated_at: string
  messages: MessageData[]
}

export interface SendMessageResponse {
  message: MessageData
  response: MessageData
}

export interface ConversationListResponse {
  conversations: ConversationListItemData[]
}

// SSE streaming event types
export interface StreamUserMessageEvent {
  type: 'user_message'
  id: number
  content: string
  created_at: string
}

export interface StreamTokenEvent {
  type: 'token'
  content: string
}

export interface StreamDoneEvent {
  type: 'done'
  emotion: string
  expression: string
  user_message_id: number
  assistant_message_id: number
}

export type StreamEvent = StreamUserMessageEvent | StreamTokenEvent | StreamDoneEvent

export interface StreamCallbacks {
  onUserMessage?: (data: StreamUserMessageEvent) => void
  onToken: (content: string) => void
  onDone: (data: StreamDoneEvent) => void
  onError: (error: Error) => void
}
