'use client'
import { FormEvent, useState } from 'react'
import { forgotPassword } from '@/lib/auth'

export default function ForgotPage() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [token, setToken] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      const data = await forgotPassword(email)
      setMessage(data.message || 'Solicitud enviada')
      if (data.reset_token) setToken(data.reset_token)
    } catch {
      setMessage('No se pudo generar recuperación')
    }
  }

  return (
    <form onSubmit={onSubmit} className="card grid gap-2">
      <h1 className="text-xl font-bold">Recuperar cuenta</h1>
      <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded border p-2" placeholder="email" />
      <button className="rounded bg-slate-900 px-3 py-2 text-xs text-white">Enviar</button>
      {message && <p className="text-xs">{message}</p>}
      {token && <p className="text-xs break-all">Token dev: {token}</p>}
    </form>
  )
}
