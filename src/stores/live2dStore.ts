import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ModelLoadState } from '@/types/live2d'

export const useLive2dStore = defineStore('live2d', () => {
  const currentExpression = ref<string>('normal')
  const currentAction = ref<string | null>(null)
  const isSpeaking = ref(false)
  const loadState = ref<ModelLoadState>({ status: 'loading', progress: 0 })

  function setExpression(name: string) { currentExpression.value = name }
  function setAction(name: string | null) { currentAction.value = name }
  function setSpeaking(speaking: boolean) { isSpeaking.value = speaking }
  function setLoadState(state: ModelLoadState) { loadState.value = state }

  return {
    currentExpression, currentAction, isSpeaking,
    loadState,
    setExpression, setAction, setSpeaking,
    setLoadState,
  }
})
