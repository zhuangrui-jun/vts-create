import type { AnimationPreset } from '@/types/live2d'

export const idlePreset: AnimationPreset = {
  name: 'idle',
  loop: true,
  duration: 4000,
  keyframes: [
    { time: 0, parameters: { ParamBreath: 0, ParamAngle_BodyY: 0, ParamAngle_HeadX: 0 } },
    { time: 1000, parameters: { ParamBreath: 0.5, ParamAngle_BodyY: 1.5, ParamAngle_HeadX: -0.8 }, easing: 'ease-in-out' },
    { time: 2000, parameters: { ParamBreath: 1.0, ParamAngle_BodyY: 0, ParamAngle_HeadX: 0.5 }, easing: 'ease-in-out' },
    { time: 3000, parameters: { ParamBreath: 0.5, ParamAngle_BodyY: -1.5, ParamAngle_HeadX: 1.2 }, easing: 'ease-in-out' },
    { time: 4000, parameters: { ParamBreath: 0, ParamAngle_BodyY: 0, ParamAngle_HeadX: 0 }, easing: 'ease-in-out' },
  ],
}
