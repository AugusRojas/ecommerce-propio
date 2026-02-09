import { Review } from '@/types'
export function ReviewCard({ review }: { review: Review }) {
  return <div className="card"><p>{'★'.repeat(review.rating)}</p><p className="text-sm">{review.comment}</p></div>
}
