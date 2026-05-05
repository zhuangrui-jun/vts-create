<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ send: [text: string] }>()
const props = defineProps<{ disabled: boolean }>()

const text = ref('')

function handleSend() {
  const trimmed = text.value.trim()
  if (!trimmed || props.disabled) return
  emit('send', trimmed)
  text.value = ''
}
</script>

<template>
  <div class="message-input">
    <input
      v-model="text"
      class="input-field"
      type="text"
      placeholder="输入消息..."
      :disabled="disabled"
      @keydown.enter="handleSend"
    />
    <button
      class="send-btn"
      :disabled="disabled || !text.trim()"
      @click="handleSend"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 2L11 13" />
        <path d="M22 2L15 22L11 13L2 9L22 2Z" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.message-input {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
}
.input-field {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--color-text-primary);
  background: var(--color-bg);
  outline: none;
  transition: border-color var(--transition-fast);
}
.input-field:focus {
  border-color: var(--color-primary);
}
.input-field:disabled {
  background: var(--color-bg-secondary);
  cursor: not-allowed;
}
.send-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  cursor: pointer;
  transition: background var(--transition-fast), opacity var(--transition-fast);
  flex-shrink: 0;
}
.send-btn:hover:not(:disabled) {
  background: var(--color-primary-dark);
}
.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
