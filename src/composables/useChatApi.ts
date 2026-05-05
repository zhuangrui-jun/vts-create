import type {
  ConversationListResponse,
  ConversationData,
  SendMessageResponse,
  ConversationListItemData,
} from '@/types/chat'

const BASE_URL = 'http://localhost:8000/api/conversations'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const detail = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(detail.detail || `API error ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export function useChatApi() {
  const listConversations = () =>
    request<ConversationListResponse>(BASE_URL)

  const createConversation = () =>
    request<ConversationListItemData>(BASE_URL, { method: 'POST' })

  const getConversation = (id: string) =>
    request<ConversationData>(`${BASE_URL}/${id}`)

  const deleteConversation = (id: string) =>
    request<void>(`${BASE_URL}/${id}`, { method: 'DELETE' })

  const sendMessage = (convId: string, content: string) =>
    request<SendMessageResponse>(`${BASE_URL}/${convId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    })

  return { listConversations, createConversation, getConversation, deleteConversation, sendMessage }
}
