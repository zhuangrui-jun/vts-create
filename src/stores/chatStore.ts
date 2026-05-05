import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useChatApi } from '@/composables/useChatApi'
import { useLive2dStore } from '@/stores/live2dStore'
import type { ConversationListItemData, MessageData } from '@/types/chat'

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
      // Update title in list if changed
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
      // Auto-create conversation if none active
      await createConversation()
      return sendMessage(content)
    }

    isSending.value = true
    error.value = null
    try {
      const result = await api.sendMessage(convId, content)
      messages.value.push(result.message)
      messages.value.push(result.response)

      // Trigger Live2D expression
      if (result.response.expression) {
        live2dStore.setExpression(result.response.expression)
      }

      // Update conversation in list (title may have changed, updated_at changed)
      const idx = conversations.value.findIndex(c => c.id === convId)
      if (idx !== -1) {
        conversations.value[idx].updated_at = result.response.created_at
      }
    } catch (e: any) {
      error.value = e.message
    } finally {
      isSending.value = false
    }
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
