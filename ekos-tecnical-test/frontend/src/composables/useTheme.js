import { ref, watchEffect } from 'vue'

const isDark = ref(
  localStorage.getItem('theme')
    ? localStorage.getItem('theme') === 'dark'
    : window.matchMedia('(prefers-color-scheme: dark)').matches
)

function applyTheme() {
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

watchEffect(applyTheme)

export function useTheme() {
  function toggle() {
    isDark.value = !isDark.value
  }
  return { isDark, toggle }
}
