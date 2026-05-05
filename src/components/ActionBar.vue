<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useLive2dStore } from '@/stores/live2dStore'
import { useLive2D } from '@/composables/useLive2D'
import type { ModelInfo } from '@/types/live2d'

const store = useLive2dStore()
const { getModelInfo, setExpression, playMotion, setScale, setOffset, resetTransform } = useLive2D()

const modelInfo = ref<ModelInfo>({ expressions: [], motions: [], hasPhysics: false, scale: 1, offsetX: 0, offsetY: 0 })
const selectedExpression = ref('normal')
const selectedMotion = ref('')

const scaleDisplay = ref(30)
const offsetXDisplay = ref(0)
const offsetYDisplay = ref(0)

// Poll model info once loaded
let pollTimer: ReturnType<typeof setInterval> | null = null

watch(() => store.loadState.status, (status) => {
  if (status === 'loaded') {
    refreshInfo()
    pollTimer = setInterval(refreshInfo, 1000)
  } else {
    if (pollTimer) clearInterval(pollTimer)
  }
}, { immediate: true })

onMounted(() => {
  if (store.loadState.status === 'loaded') refreshInfo()
})

function refreshInfo() {
  modelInfo.value = getModelInfo()
}

function handleExpressionChange() {
  setExpression(selectedExpression.value)
}

function handleMotionChange() {
  if (selectedMotion.value) {
    playMotion(selectedMotion.value)
  }
}

function handleScaleChange(delta: number) {
  const newScale = modelInfo.value.scale + delta
  setScale(newScale)
  scaleDisplay.value = Math.round(newScale * 100)
  refreshInfo()
}

function handleOffsetXChange(delta: number) {
  const newX = modelInfo.value.offsetX + delta
  setOffset(newX, modelInfo.value.offsetY)
  offsetXDisplay.value = Math.round(newX)
  refreshInfo()
}

function handleOffsetYChange(delta: number) {
  const newY = modelInfo.value.offsetY + delta
  setOffset(modelInfo.value.offsetX, newY)
  offsetYDisplay.value = Math.round(newY)
  refreshInfo()
}

function handleReset() {
  resetTransform()
  selectedExpression.value = 'normal'
  selectedMotion.value = ''
  setExpression('normal')
  scaleDisplay.value = 30
  offsetXDisplay.value = 0
  offsetYDisplay.value = 0
  refreshInfo()
}
</script>

<template>
  <div class="action-bar">
    <!-- Row 1: Expressions & Motions dropdowns -->
    <div class="row">
      <div class="group">
        <label class="label">表情</label>
        <select
          v-model="selectedExpression"
          class="select"
          @change="handleExpressionChange"
        >
          <option value="normal">正常</option>
          <option v-for="exp in modelInfo.expressions" :key="exp" :value="exp">
            {{ exp }}
          </option>
        </select>
      </div>

      <div class="group">
        <label class="label">动作</label>
        <select
          v-model="selectedMotion"
          class="select"
          @change="handleMotionChange"
        >
          <option value="">—</option>
          <option v-for="motion in modelInfo.motions" :key="motion" :value="motion">
            {{ motion }}
          </option>
        </select>
        <span v-if="modelInfo.motions.length === 0" class="hint">模型无内置动作</span>
      </div>
    </div>

    <!-- Row 2: Scale & Position controls -->
    <div class="row">
      <div class="group">
        <label class="label">缩放</label>
        <div class="stepper">
          <button class="step-btn" @click="handleScaleChange(-0.05)">−</button>
          <span class="step-val">{{ scaleDisplay }}%</span>
          <button class="step-btn" @click="handleScaleChange(0.05)">+</button>
        </div>
      </div>

      <div class="group">
        <label class="label">水平</label>
        <div class="stepper">
          <button class="step-btn" @click="handleOffsetXChange(-10)">◂</button>
          <span class="step-val">{{ offsetXDisplay }}</span>
          <button class="step-btn" @click="handleOffsetXChange(10)">▸</button>
        </div>
      </div>

      <div class="group">
        <label class="label">垂直</label>
        <div class="stepper">
          <button class="step-btn" @click="handleOffsetYChange(-10)">▴</button>
          <span class="step-val">{{ offsetYDisplay }}</span>
          <button class="step-btn" @click="handleOffsetYChange(10)">▾</button>
        </div>
      </div>

      <button class="reset-btn" @click="handleReset">重置</button>
    </div>
  </div>
</template>

<style scoped>
.action-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px 14px;
  background: linear-gradient(to top, rgba(252, 250, 245, 0.96), rgba(252, 250, 245, 0.75));
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 5;
}
.row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.group {
  display: flex;
  align-items: center;
  gap: 4px;
}
.label {
  font-size: 11px;
  color: var(--color-text-secondary);
  white-space: nowrap;
}
.select {
  padding: 3px 6px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
  font-size: 11px;
  font-family: var(--font-sans);
  cursor: pointer;
  outline: none;
}
.select:focus {
  border-color: var(--color-accent);
}
.hint {
  font-size: 10px;
  color: var(--color-text-secondary);
  opacity: 0.6;
}
.stepper {
  display: flex;
  align-items: center;
  gap: 2px;
}
.step-btn {
  width: 22px;
  height: 22px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  font-family: var(--font-sans);
}
.step-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent-dark);
}
.step-val {
  font-size: 11px;
  color: var(--color-text-secondary);
  min-width: 36px;
  text-align: center;
}
.reset-btn {
  padding: 4px 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg-elevated);
  color: var(--color-text-secondary);
  font-size: 11px;
  cursor: pointer;
  font-family: var(--font-sans);
  margin-left: auto;
}
.reset-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent-dark);
}
</style>
