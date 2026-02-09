'use client'
import { create } from 'zustand'
import { CartItem, Product } from '@/types'

type State = { items: CartItem[]; addItem: (p: Product) => void; removeItem: (id: string) => void; updateQty: (id: string, q: number) => void }
export const useCartStore = create<State>((set) => ({
  items: [],
  addItem: (p) => set((s) => {
    const existing = s.items.find((i) => i.id === p.id)
    if (existing) return { items: s.items.map((i) => i.id === p.id ? { ...i, quantity: i.quantity + 1 } : i) }
    return { items: [...s.items, { ...p, quantity: 1 }] }
  }),
  removeItem: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
  updateQty: (id, q) => set((s) => ({ items: s.items.map((i) => i.id === id ? { ...i, quantity: Math.max(1, q) } : i) }))
}))
