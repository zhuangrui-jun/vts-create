<script setup lang="ts">
import { ref } from 'vue'
import Live2DCanvas from '@/components/Live2DCanvas.vue'
import ChatPanel from '@/components/chat/ChatPanel.vue'
import IntroductionModal from '@/components/IntroductionModal.vue'

const introRef = ref<InstanceType<typeof IntroductionModal>>()
</script>

<template>
  <div class="app-layout">
    <div class="live2d-pane">
      <Live2DCanvas />
    </div>
    <div class="chat-pane">
      <IntroductionModal ref="introRef" />
      <ChatPanel />
    </div>
    <button class="intro-tip" @click="introRef?.open()" title="项目简介">?</button>
  </div>
</template>

<style scoped>
.intro-tip {
  position: fixed;
  top: 10px;
  left: 12px;
  z-index: 100;
  width: 26px;
  height: 26px;
  border: 1px solid var(--color-border, #444);
  border-radius: 50%;
  background: var(--color-bg, #1a1a2e);
  color: #999;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: .5;
  transition: opacity .15s, color .15s;
}
.intro-tip:hover {
  opacity: 1;
  color: #fff;
}
.app-layout {
  display: flex;
  width: 100%;
  height: 100%;
  background: var(--color-bg);
}
.live2d-pane {
  flex: 0 0 35%;
  min-width: 0;
  height: 100%;
  position: relative;
}
.chat-pane {
  flex: 1;
  height: 100%;
  min-width: 0;
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
