# Proyecto Ecommerce Propio

Implementación inicial del e-commerce enfocada en autenticación y cuentas de usuario:

- Registro de usuarios con contraseña hasheada (bcrypt nativo, compatible con Python 3.14).
- Login JWT (access + refresh token).
- Flujo de recuperación/restablecimiento de contraseña.
- Carrito propio por usuario creado automáticamente al registrarse.
- Frontend con Next.js para login, registro y recuperación.

## Estructura

- `frontend/`: app Next.js 14 (App Router)
- `backend/`: API FastAPI

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Variables recomendadas (`backend/.env`):

```env
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:3000
```

Seed:

```bash
cd backend
PYTHONPATH=. python scripts/seed.py
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Variables (`frontend/.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=another-secret
```

## Endpoints implementados (fase 1)

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`
- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password`
- `GET /api/cart`

## Nota

No se guarda ninguna tarjeta de pago. Solo se almacenan credenciales seguras (password hash) y datos propios del usuario.


## Compatibilidad Python 3.14

El backend está ajustado para Python **3.14+** usando dependencias compatibles:

- `psycopg[binary]` (reemplaza `psycopg2-binary`)
- `PyJWT` (reemplaza `python-jose`)
- `bcrypt` nativo (sin `passlib`)

