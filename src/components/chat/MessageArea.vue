<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import TypingIndicator from './TypingIndicator.vue'

const store = useChatStore()
const listRef = ref<HTMLDivElement>()

async function scrollToBottom() {
  await nextTick()
  if (listRef.value) {
    listRef.value.scrollTop = listRef.value.scrollHeight
  }
}

watch(() => store.messages.length, scrollToBottom)
watch(() => store.isSending, (sending) => {
  if (sending) scrollToBottom()
})
</script>

<template>
  <div class="message-area">
    <div v-if="!store.activeConversationId" class="empty-chat">
      <div class="empty-icon">💬</div>
      <div class="empty-text">选择一个对话或创建新对话开始聊天</div>
    </div>

    <div v-else ref="listRef" class="message-list">
      <div
        v-for="msg in store.messages"
        :key="msg.id"
        class="message-row"
        :class="msg.role"
      >
        <div class="avatar">
          {{ msg.role === 'user' ? '🙂' : '🌸' }}
        </div>
        <div class="bubble" :class="msg.role">
          {{ msg.content }}
          <img
            v-if="msg.role === 'assistant' && msg.sticker_path"
            :src="'http://localhost:8000/' + msg.sticker_path"
            :alt="msg.sticker_file_name || 'sticker'"
            class="sticker-img"
          />
        </div>
      </div>

      <TypingIndicator v-if="store.isSending" />

      <div v-if="store.error" class="error-banner">
        {{ store.error }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--color-text-secondary);
}
.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}
.empty-text {
  font-size: 14px;
}
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.message-row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}
.message-row.user {
  flex-direction: row-reverse;
}
.avatar {
  width: 32px;
  height: 32px;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: var(--radius-full);
  background: var(--color-bg-secondary);
}
.bubble {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
.bubble.user {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  border-bottom-right-radius: 4px;
}
.bubble.assistant {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-bottom-left-radius: 4px;
}
.sticker-img {
  display: block;
  max-width: 160px;
  margin-top: 8px;
  border-radius: var(--radius-sm);
}
.error-banner {
  padding: 8px 14px;
  background: var(--color-error);
  color: var(--color-text-on-primary);
  border-radius: var(--radius-sm);
  font-size: 13px;
}
</style>
