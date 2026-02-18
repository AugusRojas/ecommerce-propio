import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'Propio Ecommerce',
  description: 'Autenticación y carrito por usuario',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
