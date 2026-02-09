import { ReviewCard } from '@/components/ReviewCard'
import { ReviewForm } from '@/components/ReviewForm'

export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const reviews = [{ id: '1', rating: 5, comment: 'Excelente producto' }]
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9" alt="producto" className="card h-80 w-full object-cover" />
      <section className="grid gap-3">
        <h1 className="text-2xl font-bold">Producto #{params.id}</h1>
        <p>Detalle con galería, stock y precio.</p>
        <ReviewForm />
        {reviews.map((r) => <ReviewCard key={r.id} review={r} />)}
      </section>
    </div>
  )
}
