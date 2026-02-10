# Proyecto E-commerce (Next.js + FastAPI)

E-commerce full-stack con frontend en **Next.js 14 + TypeScript + Tailwind + Zustand** y backend en **FastAPI + SQLAlchemy + Supabase Postgres + JWT**, incluyendo base para Mercado Pago, reviews, órdenes y panel admin.

## Requisitos previos
- Node.js 20+
- Python 3.14+
- Cuenta de Supabase (proyecto creado)

## Instalación
### 1) Configurar Supabase
1. Crear proyecto en Supabase.
2. Ir a **Project Settings > Database** y copiar la cadena de conexión del pooler.
3. Configurar `DATABASE_URL` en `backend/.env` con la URL del pooler:
   - `DATABASE_URL=postgresql+psycopg://...?...sslmode=require`
4. Mantener `DB_USE_NULL_POOL=true` (evita doble pooling cliente + pooler).
5. (Opcional) Cargar `docs/init.sql` en el SQL Editor de Supabase.

### 2) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 3) Frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

## Variables de entorno
- Frontend: `frontend/.env.local.example`
- Backend: `backend/.env.example`

## Estructura
- `frontend/`: App Router pages, componentes UI, stores Zustand, utilidades API.
- `backend/`: API REST, modelos SQLAlchemy, schemas Pydantic, servicios y rutas.
- `docs/`: SQL inicial y colección Postman.

## Scripts útiles
- Seed data: `cd backend && python scripts/seed.py`
- Tests backend: `cd backend && pytest`

## Mercado Pago (guía rápida)
1. Crear cuenta en Mercado Pago Developers.
2. Copiar `ACCESS_TOKEN` y `PUBLIC_KEY` en `.env` y `.env.local`.
3. Configurar webhook a `POST /api/webhooks/mercadopago`.
4. Probar en sandbox con credenciales de prueba.

## Docker Compose
`docker-compose.yml` levanta **frontend + backend**. La base de datos es exclusivamente Supabase web vía `DATABASE_URL` (no hay fallback local).

## Entregables incluidos
- Código frontend y backend.
- README + pasos de instalación.
- SQL inicial: `docs/init.sql`.
- Seed data: `backend/scripts/seed.py`.
- Collection Postman: `docs/postman_collection.json`.
- Docker Compose del stack completo: `docker-compose.yml`.


## Nota sobre SQLAlchemy + Supabase
Si estabas usando `postgresql+psycopg2://...`, cámbialo a `postgresql+psycopg://...` para compatibilidad con este proyecto y Python 3.14.
