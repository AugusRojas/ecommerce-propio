import { ProductCard } from '@/components/ProductCard'

const products = Array.from({ length: 8 }).map((_, i) => ({
  id: String(i + 1),
  name: `Producto ${i + 1}`,
  description: 'Descripción detallada',
  price: 5000 + i * 1200,
  stock: 20,
  images: ['https://images.unsplash.com/photo-1491553895911-0055eca6402d']
}))

export default function ProductsPage() {
  return <div className="grid gap-4 md:grid-cols-3">{products.map((p) => <ProductCard key={p.id} product={p} />)}</div>
}
