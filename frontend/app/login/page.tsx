'use client'
import { FormEvent, useState } from 'react'
import { login } from '@/lib/auth'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      await login(email, password)
      setMessage('Login exitoso')
    } catch {
      setMessage('Error de login')
    }
  }

  return (
    <form onSubmit={onSubmit} className="card grid gap-2">
      <h1 className="text-xl font-bold">Login</h1>
      <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded border p-2" placeholder="email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} className="rounded border p-2" placeholder="password" type="password" />
      <button className="rounded bg-slate-900 px-3 py-2 text-xs text-white">Ingresar</button>
      <a className="text-xs underline" href="/recuperar-cuenta">Olvidé mi contraseña</a>
      {message && <p className="text-xs">{message}</p>}
    </form>
  )
}
