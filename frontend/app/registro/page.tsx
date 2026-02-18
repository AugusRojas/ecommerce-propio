'use client';

import { FormEvent, useState } from 'react';
import api from '@/lib/api';

export default function RegistroPage() {
  const [form, setForm] = useState({ email: '', password: '', first_name: '', last_name: '' });
  const [message, setMessage] = useState('');

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    try {
      await api.post('/api/auth/register', form);
      setMessage('Registro exitoso. Ya tenés carrito propio.');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'No se pudo registrar.');
    }
  };

  return (
    <main>
      <div className="card">
        <h1>Registro</h1>
        <form onSubmit={onSubmit}>
          <label>Nombre</label>
          <input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} required />
          <label>Apellido</label>
          <input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} required />
          <label>Email</label>
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <label>Contraseña</label>
          <input type="password" minLength={8} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <button type="submit">Crear cuenta</button>
        </form>
        <p>{message}</p>
      </div>
    </main>
  );
}
