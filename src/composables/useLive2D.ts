import { shallowRef } from 'vue'
import * as PIXI from 'pixi.js'
import { Live2DModel } from 'pixi-live2d-display/cubism4'
import { ParameterInterpolator } from '@/engine/parameter-interpolator'
import { idlePreset } from '@/engine/animation-presets'
import { getExpressionParams } from '@/engine/expression-registry'
import { useLive2dStore } from '@/stores/live2dStore'
import type { ModelInfo } from '@/types/live2d'

;(window as any).PIXI = PIXI

const DEFAULT_MODEL_PATH = '/models/yachiyo/八千代辉夜姬.model3.json'

function resolveModelPath(): string {
  return import.meta.env.VITE_MODEL_PATH || DEFAULT_MODEL_PATH
}

// Singleton state
const model = shallowRef<Live2DModel | null>(null)
const app = shallowRef<PIXI.Application | null>(null)
const interpolator = new ParameterInterpolator()
let animFrameId = 0

// User-adjustable model transform
let userScale = 0.3
let userOffsetX = 0
let userOffsetY = 0

// Dynamic model data
let modelExpressions: string[] = []
let modelMotions: string[] = []

export function useLive2D() {
  const store = useLive2dStore()

  async function init(canvas: HTMLCanvasElement, modelPath?: string): Promise<void> {
    store.setLoadState({ status: 'loading', progress: 0 })

    try {
      const containerWidth = canvas.parentElement?.clientWidth || 800
      const containerHeight = canvas.parentElement?.clientHeight || 600

      const pixiApp = new PIXI.Application({
        view: canvas,
        width: containerWidth,
        height: containerHeight,
        backgroundAlpha: 0,
        backgroundColor: 0xFCFAF5,
        antialias: true,
        resolution: window.devicePixelRatio || 1,
        autoDensity: true,
      })
      app.value = pixiApp

      store.setLoadState({ status: 'loading', progress: 30 })

      const path = modelPath || resolveModelPath()
      const live2dModel = await Live2DModel.from(path, {
        autoUpdate: true,
        autoHitTest: true,
        autoFocus: false,
        ticker: PIXI.Ticker.shared,
      })

      model.value = live2dModel
      store.setLoadState({ status: 'loading', progress: 70 })

      // Read model capabilities
      readModelCapabilities(live2dModel)

      // Position and scale
      live2dModel.anchor.set(0.5, 0.5)
      applyTransform(live2dModel, containerWidth, containerHeight)

      // Manual focus tracking — coordinates transform through model's worldTransform
      canvas.addEventListener('pointermove', (e) => {
        const rect = canvas.getBoundingClientRect()
        const view = pixiApp.renderer
        const sx = (e.clientX - rect.left) * (view.width / rect.width)
        const sy = (e.clientY - rect.top) * (view.height / rect.height)
        live2dModel.focus(sx, sy)
      })

      // Click → use first available motion or idle
      live2dModel.eventMode = 'static'
      live2dModel.cursor = 'pointer'
      live2dModel.on('pointerdown', () => {
        if (modelMotions.length > 0) {
          playRandomMotion()
        }
      })

      pixiApp.stage.addChild(live2dModel)

      store.setLoadState({ status: 'loaded', progress: 100 })

      // Idle breathing
      interpolator.startAnimation(idlePreset)
      tick()

      // Native idle motion
      playNativeIdleIfAvailable(live2dModel)

    } catch (e) {
      store.setLoadState({
        status: 'error',
        progress: 0,
        errorMessage: e instanceof Error ? e.message : '模型加载失败',
      })
    }
  }

  function readModelCapabilities(m: Live2DModel): void {
    const settings = (m.internalModel as any)?.settings

    // Expressions — CubismModelSettingsJson puts these as `settings.expressions`
    modelExpressions = []
    try {
      if (Array.isArray(settings?.expressions)) {
        modelExpressions = settings.expressions
          .map((e: any) => e.Name || e.name || '')
          .filter(Boolean)
      }
    } catch { /* ignore */ }

    // Motions — CubismModelSettingsJson puts these as `settings.motions`
    modelMotions = []
    try {
      if (settings?.motions && typeof settings.motions === 'object') {
        modelMotions = Object.keys(settings.motions).filter(k => {
          const files = settings.motions[k]
          return Array.isArray(files) && files.length > 0
        })
      }
    } catch { /* ignore */ }

    console.log('[Live2D] Expressions:', modelExpressions)
    console.log('[Live2D] Motions:', modelMotions)
  }

  function getModelInfo(): ModelInfo {
    return {
      expressions: [...modelExpressions],
      motions: [...modelMotions],
      hasPhysics: !!model.value?.internalModel && !!(model.value.internalModel as any).coreModel,
      scale: userScale,
      offsetX: userOffsetX,
      offsetY: userOffsetY,
    }
  }

  function applyTransform(m: Live2DModel, w: number, h: number): void {
    const baseScale = Math.min(w / 2000, h / 2400)
    m.scale.set(baseScale * userScale)
    m.position.set(w / 2 + userOffsetX, h * 0.55 + userOffsetY)
  }

  function setScale(scale: number): void {
    userScale = Math.max(0.3, Math.min(3, scale))
    const m = model.value
    if (m && app.value) {
      applyTransform(m, app.value.screen.width, app.value.screen.height)
    }
  }

  function setOffset(x: number, y: number): void {
    userOffsetX = x
    userOffsetY = y
    const m = model.value
    if (m && app.value) {
      applyTransform(m, app.value.screen.width, app.value.screen.height)
    }
  }

  function resetTransform(): void {
    userScale = 0.3
    userOffsetX = 0
    userOffsetY = 0
    const m = model.value
    if (m && app.value) {
      applyTransform(m, app.value.screen.width, app.value.screen.height)
    }
  }

  // --- Expression control ---

  async function setExpression(name: string): Promise<void> {
    store.setExpression(name)
    interpolator.clearExpression()

    const m = model.value
    if (!m) return

    // Reset to default expression
    if (!name || name === 'normal') {
      try {
        const mgr = (m.internalModel as any)?.expressionManager
        if (mgr?.resetExpression) {
          mgr.resetExpression()
        }
      } catch { /* ignore */ }
      return
    }

    // Primary: native expression API (loads .exp3.json + applies CubismExpressionMotion)
    try {
      const result = await m.expression(name)
      console.log('[Live2D] native expression:', name, '→', result ? 'OK' : 'not found')
      if (result) return
    } catch (e) {
      console.warn('[Live2D] native expression failed:', e)
    }

    // Fallback: direct parameter manipulation
    const params = getExpressionParams(name)
    console.log('[Live2D] setExpression fallback:', name, '→ params:', params)
    if (params && Object.keys(params).length > 0) {
      interpolator.setExpression(params)
      if (m.internalModel) {
        const core = m.internalModel.coreModel as Record<string, any>
        for (const [id, value] of Object.entries(params)) {
          try { core.setParameterValue(id, value) } catch { /* skip */ }
        }
      }
    }
  }

  // --- Motion control ---

  function playMotion(group: string, index?: number): void {
    const m = model.value
    if (!m) return

    store.setAction(group)

    try {
      const mgr = (m.internalModel as any)?.motionManager
      if (mgr?.startMotion) {
        if (index !== undefined) {
          mgr.startMotion(group, index, 3) // FORCE priority
        } else {
          mgr.startRandomMotion(group, 3)
        }
        return
      }
    } catch { /* native motion failed */ }
  }

  function playRandomMotion(): void {
    if (modelMotions.length === 0) return
    const group = modelMotions[Math.floor(Math.random() * modelMotions.length)]
    playMotion(group)
  }

  function stopMotion(): void {
    store.setAction(null)
    const m = model.value
    if (m) {
      try {
        const mgr = (m.internalModel as any)?.motionManager
        mgr?.stopAllMotions?.()
      } catch { /* ignore */ }
    }
  }

  // --- Speaking ---

  function setSpeaking(speaking: boolean): void {
    store.setSpeaking(speaking)
    interpolator.setSpeaking(speaking)
  }

  // --- Internal ---

  function playNativeIdleIfAvailable(m: Live2DModel): void {
    const idleGroup = modelMotions.find(g => g.toLowerCase().includes('idle'))
    if (idleGroup) {
      playMotion(idleGroup)
    }
  }

  function tick(): void {
    const now = performance.now()
    const params = interpolator.update(now)

    const m = model.value
    if (m?.internalModel) {
      const core = m.internalModel.coreModel as Record<string, any>
      for (const [id, value] of Object.entries(params)) {
        try {
          if (typeof core.setParameterValue === 'function') {
            core.setParameterValue(id, value)
          }
        } catch { /* skip */ }
      }
    }

    animFrameId = requestAnimationFrame(tick)
  }

  function handleResize(width: number, height: number): void {
    app.value?.renderer.resize(width, height)
    const m = model.value
    if (m) {
      applyTransform(m, width, height)
    }
  }

  function destroy(): void {
    cancelAnimationFrame(animFrameId)
    interpolator.clearAllAnimations()
    model.value?.destroy()
    app.value?.destroy(true)
    model.value = null
    app.value = null
    modelExpressions = []
    modelMotions = []
    userScale = 0.3
    userOffsetX = 0
    userOffsetY = 0
  }

  return {
    model,
    init,
    destroy,
    getModelInfo,
    setExpression,
    playMotion,
    playRandomMotion,
    stopMotion,
    setSpeaking,
    setScale,
    setOffset,
    resetTransform,
    handleResize,
  }
}
