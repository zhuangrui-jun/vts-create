<script setup lang="ts">
import { useChatStore } from '@/stores/chatStore'

const store = useChatStore()

function handleDelete(id: string) {
  if (confirm('确定要删除这个对话吗？')) {
    store.deleteConversation(id)
  }
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <button class="new-btn" @click="store.createConversation()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12h14" />
        </svg>
        新对话
      </button>
    </div>

    <div class="conversation-list">
      <div v-if="store.conversations.length === 0" class="empty-state">
        暂无对话，点击上方按钮开始
      </div>
      <div
        v-for="conv in store.conversations"
        :key="conv.id"
        class="conv-item"
        :class="{ active: conv.id === store.activeConversationId }"
        @click="store.selectConversation(conv.id)"
      >
        <div class="conv-info">
          <div class="conv-title">{{ conv.title }}</div>
          <div class="conv-time">{{ new Date(conv.updated_at).toLocaleString() }}</div>
        </div>
        <button class="delete-btn" @click.stop="handleDelete(conv.id)" title="删除对话">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2" />
          </svg>
        </button>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: 260px;
  background: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  flex-shrink: 0;
}
.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
}
.new-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 10px 0;
  border: 1px dashed var(--color-primary);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-primary);
  font-size: 14px;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: background var(--transition-fast);
}
.new-btn:hover {
  background: var(--color-primary-light);
  color: var(--color-text-on-primary);
}
.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px;
}
.empty-state {
  padding: 24px 16px;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 13px;
}
.conv-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition-fast);
  gap: 8px;
}
.conv-item:hover {
  background: var(--color-border-light);
}
.conv-item.active {
  background: var(--color-primary-light);
}
.conv-info {
  flex: 1;
  min-width: 0;
}
.conv-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.conv-time {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 2px;
}
.delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  opacity: 0;
  transition: opacity var(--transition-fast), background var(--transition-fast);
  flex-shrink: 0;
}
.conv-item:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  background: var(--color-error);
  color: var(--color-text-on-primary);
}
</style>
