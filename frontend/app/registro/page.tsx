'use client'
import { FormEvent, useState } from 'react'
import { register } from '@/lib/auth'

export default function RegisterPage() {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      await register({ first_name: firstName, last_name: lastName, email, password })
      setMessage('Registro exitoso')
    } catch {
      setMessage('Error de registro')
    }
  }

  return (
    <form onSubmit={onSubmit} className="card grid gap-2">
      <h1 className="text-xl font-bold">Registro</h1>
      <input value={firstName} onChange={(e) => setFirstName(e.target.value)} className="rounded border p-2" placeholder="nombre" />
      <input value={lastName} onChange={(e) => setLastName(e.target.value)} className="rounded border p-2" placeholder="apellido" />
      <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded border p-2" placeholder="email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} className="rounded border p-2" placeholder="password" type="password" />
      <button className="rounded bg-slate-900 px-3 py-2 text-xs text-white">Crear cuenta</button>
      {message && <p className="text-xs">{message}</p>}
    </form>
  )
}
