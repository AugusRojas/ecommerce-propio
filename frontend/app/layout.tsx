import './globals.css'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Propio Shop',
  description: 'E-commerce moderno con Next.js + FastAPI',
  openGraph: { title: 'Propio Shop', description: 'Tienda online completa' }
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Header />
        <main className="mx-auto min-h-screen max-w-6xl px-4 py-8">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
