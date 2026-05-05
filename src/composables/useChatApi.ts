import type {
  ConversationListResponse,
  ConversationData,
  ConversationListItemData,
  StreamCallbacks,
  StreamEvent,
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

  const sendMessageStream = async (convId: string, content: string, callbacks: StreamCallbacks) => {
    try {
      const res = await fetch(`${BASE_URL}/${convId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      })
      if (!res.ok) {
        const detail = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(detail.detail || `API error ${res.status}`)
      }
      const reader = res.body?.getReader()
      if (!reader) throw new Error('No response body')

      const decoder = new TextDecoder()
      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data: StreamEvent = JSON.parse(line.slice(6))
            switch (data.type) {
              case 'user_message':
                callbacks.onUserMessage?.(data)
                break
              case 'token':
                callbacks.onToken(data.content)
                break
              case 'done':
                callbacks.onDone(data)
                break
            }
          }
        }
      }
    } catch (e: any) {
      callbacks.onError(e)
    }
  }

  return { listConversations, createConversation, getConversation, deleteConversation, sendMessageStream }
}
