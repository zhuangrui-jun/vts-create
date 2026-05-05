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
