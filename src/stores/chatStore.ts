import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useChatApi } from '@/composables/useChatApi'
import { useLive2dStore } from '@/stores/live2dStore'
import type { ConversationListItemData, MessageData } from '@/types/chat'

let _nextOptimisticId = -1

export const useChatStore = defineStore('chat', () => {
  const api = useChatApi()
  const live2dStore = useLive2dStore()

  const conversations = ref<ConversationListItemData[]>([])
  const activeConversationId = ref<string | null>(null)
  const messages = ref<MessageData[]>([])
  const isLoading = ref(false)
  const isSending = ref(false)
  const error = ref<string | null>(null)

  const activeConversation = computed(() =>
    conversations.value.find(c => c.id === activeConversationId.value) ?? null,
  )

  async function loadConversations() {
    isLoading.value = true
    error.value = null
    try {
      const data = await api.listConversations()
      conversations.value = data.conversations
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function createConversation() {
    error.value = null
    try {
      const conv = await api.createConversation()
      conversations.value.unshift(conv)
      activeConversationId.value = conv.id
      messages.value = []
    } catch (e: any) {
      error.value = e.message
    }
  }

  async function selectConversation(id: string) {
    error.value = null
    isLoading.value = true
    try {
      const conv = await api.getConversation(id)
      activeConversationId.value = id
      messages.value = conv.messages
      const idx = conversations.value.findIndex(c => c.id === id)
      if (idx !== -1) {
        conversations.value[idx] = {
          id: conv.id,
          title: conv.title,
          created_at: conv.created_at,
          updated_at: conv.updated_at,
        }
      }
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function deleteConversation(id: string) {
    error.value = null
    try {
      await api.deleteConversation(id)
      conversations.value = conversations.value.filter(c => c.id !== id)
      if (activeConversationId.value === id) {
        activeConversationId.value = null
        messages.value = []
      }
    } catch (e: any) {
      error.value = e.message
    }
  }

  async function sendMessage(content: string) {
    const convId = activeConversationId.value
    if (!convId) {
      await createConversation()
      return sendMessage(content)
    }

    isSending.value = true
    error.value = null

    // Optimistic user message
    const optimisticUserMsg: MessageData = {
      id: _nextOptimisticId--,
      conversation_id: convId,
      role: 'user',
      content,
      emotion: null,
      expression: null,
      created_at: new Date().toISOString(),
    }
    messages.value.push(optimisticUserMsg)

    // Placeholder assistant message
    const assistantMsg: MessageData = {
      id: _nextOptimisticId--,
      conversation_id: convId,
      role: 'assistant',
      content: '',
      emotion: null,
      expression: null,
      created_at: new Date().toISOString(),
    }
    messages.value.push(assistantMsg)

    await api.sendMessageStream(convId, content, {
      onUserMessage(data) {
        // Replace optimistic user message with real one
        const idx = messages.value.findIndex(m => m.id === optimisticUserMsg.id)
        if (idx !== -1) {
          messages.value[idx] = { ...messages.value[idx], id: data.id, created_at: data.created_at }
        }
      },
      onToken(token) {
        // Find the last assistant message (placeholder) and append
        const last = messages.value[messages.value.length - 1]
        if (last && last.role === 'assistant') {
          last.content += token
        }
      },
      onDone(data) {
        // Update assistant message with final metadata
        const last = messages.value[messages.value.length - 1]
        if (last && last.role === 'assistant') {
          last.id = data.assistant_message_id
          last.emotion = data.emotion
          last.expression = data.expression
        }
        // Trigger Live2D expression
        if (data.expression) {
          live2dStore.setExpression(data.expression)
        }
        // Refresh conversation list (title/updated_at may have changed)
        const idx = conversations.value.findIndex(c => c.id === convId)
        if (idx !== -1) {
          conversations.value[idx] = {
            ...conversations.value[idx],
            updated_at: new Date().toISOString(),
          }
        }
        isSending.value = false
      },
      onSticker(data) {
        const last = messages.value[messages.value.length - 1]
        if (last && last.role === 'assistant') {
          last.sticker_path = data.path
          last.sticker_file_name = data.file_name
        }
      },
      onError(err) {
        // Remove optimistic messages on error
        messages.value = messages.value.filter(
          m => m.id !== optimisticUserMsg.id && m.id !== assistantMsg.id,
        )
        error.value = err.message
        isSending.value = false
      },
    })
  }

  function clearError() {
    error.value = null
  }

  return {
    conversations,
    activeConversationId,
    activeConversation,
    messages,
    isLoading,
    isSending,
    error,
    loadConversations,
    createConversation,
    selectConversation,
    deleteConversation,
    sendMessage,
    clearError,
  }
})
