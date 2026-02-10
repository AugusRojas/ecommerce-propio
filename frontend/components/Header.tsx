import Link from 'next/link'
import { ThemeToggle } from './ThemeToggle'

export function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/50 bg-white/80 backdrop-blur dark:border-slate-700 dark:bg-slate-900/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="font-bold">Propio Shop</Link>
        <nav className="flex gap-4 text-sm">
          <Link href="/productos">Productos</Link>
          <Link href="/carrito">Carrito</Link>
          <Link href="/perfil">Perfil</Link>
        </nav>
        <ThemeToggle />
      </div>
    </header>
  )
}
