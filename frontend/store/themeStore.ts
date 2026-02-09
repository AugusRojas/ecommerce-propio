'use client'
import { create } from 'zustand'

type ThemeState = { dark: boolean; toggle: () => void }
export const useThemeStore = create<ThemeState>((set) => ({ dark: false, toggle: () => set((s) => {
  const dark = !s.dark
  if (typeof document !== 'undefined') document.documentElement.classList.toggle('dark', dark)
  return { dark }
}) }))
