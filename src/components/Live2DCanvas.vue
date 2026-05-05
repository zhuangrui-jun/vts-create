<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useLive2D } from '@/composables/useLive2D'
import { useLive2dStore } from '@/stores/live2dStore'
import LoadOverlay from './LoadOverlay.vue'
import ActionBar from './ActionBar.vue'

const containerRef = ref<HTMLDivElement>()
const canvasRef = ref<HTMLCanvasElement>()
const { init, destroy, handleResize, setExpression } = useLive2D()
const store = useLive2dStore()

let resizeObserver: ResizeObserver | null = null

// Sync store-driven expression changes to the actual model
watch(() => store.currentExpression, (name) => {
  setExpression(name)
})

onMounted(async () => {
  if (canvasRef.value) {
    await init(canvasRef.value)
  }

  if (containerRef.value) {
    resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect
        handleResize(width, height)
      }
    })
    resizeObserver.observe(containerRef.value)
  }
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  destroy()
})
</script>

<template>
  <div ref="containerRef" class="live2d-container">
    <canvas ref="canvasRef" class="live2d-canvas" />
    <LoadOverlay
      v-if="store.loadState.status !== 'loaded'"
      :status="store.loadState.status"
      :error-message="store.loadState.errorMessage"
    />
    <ActionBar v-if="store.loadState.status === 'loaded'" />
  </div>
</template>

<style scoped>
.live2d-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--color-bg);
}
.live2d-canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
