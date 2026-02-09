'use client'
import { Product } from '@/types'
import { useCartStore } from '@/store/cartStore'
import Link from 'next/link'

export function ProductCard({ product }: { product: Product }) {
  const add = useCartStore((s) => s.addItem)
  return (
    <article className="card">
      <img src={product.images[0]} alt={product.name} className="h-44 w-full rounded object-cover" />
      <h3 className="mt-3 font-semibold">{product.name}</h3>
      <p className="text-sm text-slate-500">${product.price}</p>
      <div className="mt-3 flex gap-2">
        <Link className="rounded bg-slate-900 px-3 py-2 text-xs text-white" href={`/productos/${product.id}`}>Ver</Link>
        <button className="rounded border px-3 py-2 text-xs" onClick={() => add(product)}>Agregar</button>
      </div>
    </article>
  )
}
