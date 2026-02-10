import { ProductCard } from '@/components/ProductCard'

const featured = [
  { id: '1', name: 'Auriculares Pro', description: 'Audio inmersivo', price: 19999, stock: 9, images: ['https://images.unsplash.com/photo-1505740420928-5e560c06d30e'] },
  { id: '2', name: 'Smartwatch Fit', description: 'Salud y deporte', price: 25999, stock: 12, images: ['https://images.unsplash.com/photo-1523275335684-37898b6baf30'] }
]

export default function HomePage() {
  return (
    <section className="grid gap-8">
      <div className="card bg-gradient-to-r from-indigo-600 to-cyan-500 text-white">
        <h1 className="text-3xl font-bold">Tecnología y estilo en un mismo lugar</h1>
        <p className="mt-2 text-sm">Inspirado en Vercel, Stripe y Shopify.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">{featured.map((p) => <ProductCard key={p.id} product={p} />)}</div>
    </section>
  )
}
