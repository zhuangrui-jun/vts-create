import type { AnimationPreset, AnimationChannel, EasingFunction } from '@/types/live2d'

function easeValue(t: number, easing: EasingFunction): number {
  switch (easing) {
    case 'ease-in':
      return t * t
    case 'ease-out':
      return t * (2 - t)
    case 'ease-in-out':
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
    default:
      return t
  }
}

export class ParameterInterpolator {
  private channels: Map<string, AnimationChannel> = new Map()
  private expressionOverrides: Record<string, number> = {}
  private speakingWeight = 0

  private paramValues: Record<string, number> = {}

  startAnimation(preset: AnimationPreset, weight = 1): void {
    this.channels.set(preset.name, {
      preset,
      startTime: performance.now(),
      elapsed: 0,
      weight,
    })
  }

  stopAnimation(name: string): void {
    this.channels.delete(name)
  }

  clearAllAnimations(): void {
    this.channels.clear()
  }

  setExpression(params: Record<string, number>): void {
    this.expressionOverrides = { ...params }
  }

  clearExpression(): void {
    this.expressionOverrides = {}
  }

  setSpeaking(speaking: boolean): void {
    this.speakingWeight = speaking ? 1 : 0
  }

  update(now: number): Record<string, number> {
    const result: Record<string, number> = {}

    for (const [name, channel] of this.channels) {
      const { preset, startTime, weight } = channel
      const elapsed = now - startTime
      const totalDuration = preset.duration

      if (!preset.loop && elapsed >= totalDuration) {
        if (preset.keyframes.length > 0) {
          const last = preset.keyframes[preset.keyframes.length - 1]
          for (const [id, value] of Object.entries(last.parameters)) {
            result[id] = (result[id] || 0) + value * weight
          }
        }
        this.channels.delete(name)
        continue
      }

      const loopedTime = preset.loop ? elapsed % totalDuration : Math.min(elapsed, totalDuration)

      const interpolated = this.interpolatePreset(preset, loopedTime)
      for (const [id, value] of Object.entries(interpolated)) {
        result[id] = (result[id] || 0) + value * weight
      }

      channel.elapsed = elapsed
    }

    // Apply expression overrides (highest priority for expression params)
    for (const [id, value] of Object.entries(this.expressionOverrides)) {
      result[id] = value
    }

    // Apply speaking modulation
    if (this.speakingWeight > 0) {
      const mouthValue = Math.sin(now * 0.005 * 5) * 0.3 + 0.2
      result['ParamMouthOpenY'] = (result['ParamMouthOpenY'] || 0) + mouthValue * this.speakingWeight
    }

    this.paramValues = result
    return result
  }

  private interpolatePreset(preset: AnimationPreset, time: number): Record<string, number> {
    const { keyframes } = preset
    if (keyframes.length === 0) return {}
    if (keyframes.length === 1) return { ...keyframes[0].parameters }
    if (time <= keyframes[0].time) return { ...keyframes[0].parameters }

    const last = keyframes[keyframes.length - 1]
    if (time >= last.time) return { ...last.parameters }

    let i = 0
    while (i < keyframes.length - 1 && keyframes[i + 1].time <= time) {
      i++
    }

    const kf0 = keyframes[i]
    const kf1 = keyframes[i + 1]
    const segmentDuration = kf1.time - kf0.time
    const t = segmentDuration > 0 ? (time - kf0.time) / segmentDuration : 0
    const eased = easeValue(Math.max(0, Math.min(1, t)), kf0.easing || 'linear')

    const result: Record<string, number> = {}
    const allIds = new Set([...Object.keys(kf0.parameters), ...Object.keys(kf1.parameters)])
    for (const id of allIds) {
      const v0 = kf0.parameters[id] ?? 0
      const v1 = kf1.parameters[id] ?? 0
      result[id] = v0 + (v1 - v0) * eased
    }

    return result
  }

  getCurrentValues(): Record<string, number> {
    return { ...this.paramValues }
  }
}
