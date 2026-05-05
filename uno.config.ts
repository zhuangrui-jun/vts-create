import { defineConfig, presetUno } from 'unocss'

export default defineConfig({
  presets: [presetUno()],
  theme: {
    colors: {
      primary: {
        DEFAULT: '#D4A574',
        light: '#E8C9A0',
        dark: '#B8895E',
      },
      accent: {
        DEFAULT: '#E8A0A0',
        light: '#F5D0D0',
        dark: '#C47A7A',
      },
      bg: {
        DEFAULT: '#FCFAF5',
        secondary: '#F8F3EC',
        elevated: '#FFFFFF',
      },
      ink: {
        DEFAULT: '#3D3229',
        light: '#8A7D71',
      },
      bamboo: '#8DB87C',
    },
    fontFamily: {
      sans: ['"Noto Sans SC"', '"Noto Sans JP"', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
    },
  },
})
