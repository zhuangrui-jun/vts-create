export interface AnimationKeyframe {
  time: number
  parameters: Record<string, number>
  easing?: EasingFunction
}

export type EasingFunction = 'linear' | 'ease-in' | 'ease-out' | 'ease-in-out'

export interface AnimationPreset {
  name: string
  loop: boolean
  duration: number
  keyframes: AnimationKeyframe[]
}

export interface ExpressionOverride {
  parameters: Record<string, number>
}

export interface ModelLoadState {
  status: 'loading' | 'loaded' | 'error'
  progress: number
  errorMessage?: string
}

export interface AnimationChannel {
  preset: AnimationPreset
  startTime: number
  elapsed: number
  weight: number
}

export interface ModelInfo {
  expressions: string[]
  motions: string[]
  hasPhysics: boolean
  scale: number
  offsetX: number
  offsetY: number
}
