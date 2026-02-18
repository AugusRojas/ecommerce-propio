'use client'
import { FormEvent, useState } from 'react'
import { resetPassword } from '@/lib/auth'

export default function ResetPage() {
  const [token, setToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [message, setMessage] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      const data = await resetPassword(token, newPassword)
      setMessage(data.message || 'Contraseña actualizada')
    } catch {
      setMessage('No se pudo resetear contraseña')
    }
  }

  return (
    <form onSubmit={onSubmit} className="card grid gap-2">
      <h1 className="text-xl font-bold">Restablecer cuenta</h1>
      <input value={token} onChange={(e) => setToken(e.target.value)} className="rounded border p-2" placeholder="token" />
      <input value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="rounded border p-2" placeholder="nueva contraseña" type="password" />
      <button className="rounded bg-slate-900 px-3 py-2 text-xs text-white">Restablecer</button>
      {message && <p className="text-xs">{message}</p>}
    </form>
  )
}
