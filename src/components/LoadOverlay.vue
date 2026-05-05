<script setup lang="ts">
import { useLive2dStore } from '@/stores/live2dStore'

defineProps<{
  status: string
  errorMessage?: string
}>()

const store = useLive2dStore()

function retry() {
  window.location.reload()
}
</script>

<template>
  <div class="load-overlay">
    <template v-if="status === 'loading'">
      <div class="spinner" />
      <p class="load-text">角色加载中...</p>
    </template>
    <template v-else-if="status === 'error'">
      <div class="error-icon">!</div>
      <p class="error-text">{{ errorMessage || '加载失败' }}</p>
      <button class="retry-btn" @click="retry">重新加载</button>
    </template>
  </div>
</template>

<style scoped>
.load-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  gap: 16px;
  z-index: 10;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.load-text {
  color: var(--color-text-secondary);
  font-size: 14px;
}
.error-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}
.error-text {
  color: var(--color-accent-dark);
  font-size: 14px;
}
.retry-btn {
  padding: 8px 24px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  font-size: 14px;
  cursor: pointer;
  transition: background var(--transition-fast);
}
.retry-btn:hover {
  background: var(--color-primary-dark);
}
</style>
