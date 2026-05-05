<script setup lang="ts">
import Live2DCanvas from '@/components/Live2DCanvas.vue'
</script>

<template>
  <div class="app-layout">
    <Live2DCanvas />
  </div>
</template>

<style scoped>
.app-layout {
  width: 100%;
  height: 100%;
  background: var(--color-bg);
}
</style>
