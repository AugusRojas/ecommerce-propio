export type Product = { id: string; name: string; description: string; price: number; images: string[]; stock: number }
export type Review = { id: string; rating: number; comment: string }
export type CartItem = Product & { quantity: number }
