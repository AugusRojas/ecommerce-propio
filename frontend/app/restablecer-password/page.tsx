'use client';

import { FormEvent, useState } from 'react';
import api from '@/lib/api';

export default function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');

  const requestReset = async (event: FormEvent) => {
    event.preventDefault();
    const { data } = await api.post('/api/auth/forgot-password', { email });
    if (data.reset_token) setToken(data.reset_token);
    setMessage(data.message);
  };

  const confirmReset = async (event: FormEvent) => {
    event.preventDefault();
    const { data } = await api.post('/api/auth/reset-password', { token, new_password: newPassword });
    setMessage(data.message);
  };

  return (
    <main>
      <div className="card">
        <h1>Restablecer contraseña</h1>
        <form onSubmit={requestReset}>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <button type="submit">Solicitar token</button>
        </form>

        <form onSubmit={confirmReset}>
          <label>Token</label>
          <input value={token} onChange={(e) => setToken(e.target.value)} required />
          <label>Nueva contraseña</label>
          <input type="password" minLength={8} value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
          <button type="submit">Actualizar contraseña</button>
        </form>
        <p>{message}</p>
      </div>
    </main>
  );
}
