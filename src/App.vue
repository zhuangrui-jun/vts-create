<script setup lang="ts">
import Live2DCanvas from '@/components/Live2DCanvas.vue'
import ChatPanel from '@/components/chat/ChatPanel.vue'
</script>

<template>
  <div class="app-layout">
    <div class="live2d-pane">
      <Live2DCanvas />
    </div>
    <div class="chat-pane">
      <ChatPanel />
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100%;
  background: var(--color-bg);
}
.live2d-pane {
  flex: 1;
  min-width: 0;
  height: 100%;
  position: relative;
}
.chat-pane {
  width: 400px;
  height: 100%;
  flex-shrink: 0;
  border-left: 1px solid var(--color-border);
}

@media (max-width: 767px) {
  .app-layout {
    flex-direction: column;
  }
  .live2d-pane {
    height: 50%;
  }
  .chat-pane {
    width: 100%;
    height: 50%;
  }
}
</style>
