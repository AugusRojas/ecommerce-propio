'use client'
import { useCartStore } from '@/store/cartStore'
import { CartItem } from '@/components/CartItem'

export default function CartPage() {
  const items = useCartStore((s) => s.items)
  const total = items.reduce((acc, i) => acc + i.price * i.quantity, 0)
  return <section className="grid gap-4"><h1 className="text-2xl font-bold">Carrito</h1>{items.map((i) => <CartItem key={i.id} item={i} />)}<p>Total: ${total}</p></section>
}
