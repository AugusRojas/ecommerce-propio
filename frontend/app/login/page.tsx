'use client';

import { FormEvent, useState } from 'react';
import { signIn } from 'next-auth/react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const result = await signIn('credentials', { email, password, redirect: false });
    if (result?.ok) {
      setMessage('Login correcto.');
      return;
    }
    setMessage('Email o contraseña inválidos.');
  };

  return (
    <main>
      <div className="card">
        <h1>Iniciar sesión</h1>
        <form onSubmit={onSubmit}>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Contraseña</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit">Entrar</button>
        </form>
        <p>{message}</p>
        <a href="/restablecer-password">¿Olvidaste tu contraseña?</a>
      </div>
    </main>
  );
}
