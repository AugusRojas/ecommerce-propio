'use client'
import { CartItem as CartItemType } from '@/types'
import { useCartStore } from '@/store/cartStore'

export function CartItem({ item }: { item: CartItemType }) {
  const update = useCartStore((s) => s.updateQty)
  const remove = useCartStore((s) => s.removeItem)
  return <div className="card flex items-center justify-between"><span>{item.name} x{item.quantity}</span><div className="flex gap-2"><button onClick={() => update(item.id, item.quantity + 1)}>+</button><button onClick={() => remove(item.id)}>Eliminar</button></div></div>
}
