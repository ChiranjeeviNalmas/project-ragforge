# RAGForge

Upload your docs, pick your LLM, get a production-ready RAG API in minutes.

RAGForge is a multi-tenant SaaS platform for Retrieval-Augmented Generation. Each tenant uploads their own documents, brings their own LLM API key, and gets back a shareable REST endpoint that answers questions grounded in their content — with streaming responses and source citations.

## What makes it different

- **BYOK (bring-your-own-key)** — tenants supply their own OpenAI / Claude / Gemini / Mistral API key. RAGForge never pays for tenant inference; it's pure infrastructure margin.
- **True multi-tenant isolation** — every table below the tenant level carries `tenant_id`, enforced at the application layer today and designed to move to Postgres row-level security as the project matures.
- **Local reranking, no paid dependency** — uses a local cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) instead of a hosted reranking API.
- **Encrypted secrets at rest** — tenant API keys are Fernet-encrypted before they ever touch the database.
- **Async by default** — document ingestion runs as a background job (ARQ + Redis), never blocking the request/response cycle.

## Stack

| Layer | Choice |
|---|---|
| Frontend | React + Tailwind |
| Backend | FastAPI (async) |
| RAG orchestration | LangChain |
| Vector store | pgvector on Railway PostgreSQL |
| Background jobs | ARQ + Redis |
| Auth | JWT + Fernet-encrypted API keys |

## Project status

**Week 1 of 6 — complete.**

- [x] FastAPI project skeleton
- [x] Async Postgres + pgvector connection
- [x] Core models: Tenant, User, Document, Chunk
- [x] JWT auth (`/auth/register`, `/auth/login`)
- [x] Basic document upload endpoint (`/documents/upload`)
- [ ] Background ingestion job (chunk → embed → store) — Week 2
- [ ] RAG query endpoint with streaming + citations — Week 3
- [ ] Shareable tenant endpoint URLs — Week 4
- [ ] Team roles (Owner/Admin/Viewer) — Week 5
- [ ] React admin dashboard — Week 6

## Folder structure

```
app/
├── main.py                # entrypoint — mounts routers, creates tables
├── core/
│   ├── config.py          # settings loaded from .env
│   └── security/
│       ├── password.py    # bcrypt hash/verify
│       ├── jwt.py         # token create/decode
│       └── crypto.py      # Fernet encrypt/decrypt for tenant API keys
├── db/
│   ├── base.py            # SQLAlchemy declarative base
│   └── session.py         # async engine + session factory
├── models/
│   ├── tenant.py
│   ├── user.py             # scoped by tenant_id, has role
│   ├── document.py         # scoped by tenant_id, tracks ingestion status
│   └── chunk.py            # scoped by tenant_id, holds the pgvector embedding
├── schemas/
│   ├── auth.py
│   └── document.py
└── api/
    ├── deps.py             # extracts current tenant from the JWT
    ├── documents.py        # POST /documents/upload
    └── auth/
        ├── register.py     # POST /auth/register
        ├── login.py        # POST /auth/login
        └── __init__.py     # wires both under /auth
```

## Getting started

```bash
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/ragforge
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=<random 64-char string>
FERNET_KEY=<generate below>
```

Generate a Fernet key:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Run it:

```bash
uvicorn app.main:app --reload
```

Tables are created automatically on startup for now. This is a Week 1 convenience — before adding new columns in later weeks, this project should move to Alembic migrations instead of relying on `create_all`.

## Coding conventions

This project follows a deliberately strict style, applied to every file:

- Max ~20 lines per file or logical section
- One responsibility per file — high modularity over convenience
- A single blank line between every line of code
- Only one-line comments — no docstrings, no block comments
- No unnecessary boilerplate

## API reference (current)

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Creates a new tenant + first user, returns a JWT |
| POST | `/auth/login` | Authenticates an existing user, returns a JWT |
| POST | `/documents/upload` | Accepts a file, creates a pending document record |
| GET | `/health` | Liveness check |

## Known hard problems ahead

Tracked here so they don't get forgotten as we build:

- **Chunking context loss** — naive fixed-size chunking can split a sentence or table across chunks
- **Embedding drift** — swapping embedding models later invalidates existing vectors
- **Tenant data leaks** — app-layer `tenant_id` filtering is Week 1's guardrail; Postgres RLS is the real fix
- **Cold starts** — first query against a tenant's index after inactivity
- **Async job failures** — ingestion jobs need retry/dead-letter handling, not silent failure
- **Context window overflow** — too many retrieved chunks can blow past the LLM's context limit
- **Retrieval confidence illusion** — a high similarity score doesn't guarantee an actually relevant chunk
