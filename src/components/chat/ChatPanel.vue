<script setup lang="ts">
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import ConversationSidebar from './ConversationSidebar.vue'
import MessageArea from './MessageArea.vue'
import MessageInput from './MessageInput.vue'

const store = useChatStore()

onMounted(() => {
  store.loadConversations()
})

function handleSend(text: string) {
  store.sendMessage(text)
}
</script>

<template>
  <div class="chat-panel">
    <ConversationSidebar />
    <div class="chat-main">
      <MessageArea />
      <MessageInput
        :disabled="!store.activeConversationId || store.isSending"
        @send="handleSend"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-panel {
  display: flex;
  height: 100%;
  background: var(--color-bg);
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
</style>
