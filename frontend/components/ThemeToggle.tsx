'use client'
import { useThemeStore } from '@/store/themeStore'

export function ThemeToggle() {
  const { dark, toggle } = useThemeStore()
  return <button onClick={toggle} className="rounded border px-2 py-1 text-xs">{dark ? '☀️' : '🌙'}</button>
}
