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
| Evals | Custom harness (`eval/`), scored against labeled fixture sets |

## Project status

Three tracks build in parallel: **Backend**, **Frontend**, and **Evals**. Each step ships one narrow slice and isn't considered done until its own eval (or, for Eval-track steps, its self-check) passes. A backend/frontend step that depends on an eval (e.g. chunking, retrieval, reranking) doesn't get checked off until the corresponding Eval-track step exists and is green — the two tracks move together, not backend-first-then-evaluated-later.

### Backend

- [ ] **Step 1 — Project skeleton.** Build: FastAPI app boots, `/health` returns 200. Check: `curl localhost:8000/health` → `{"status": "ok"}`.
- [ ] **Step 2 — Async Postgres + pgvector connection.** Build: async SQLAlchemy engine connects to Railway Postgres, `pgvector` extension enabled. Check: startup script runs `SELECT 1` and `SELECT * FROM pg_extension WHERE extname='vector'` successfully.
- [ ] **Step 3 — Core models.** Build: `Tenant`, `User`, `Document`, `Chunk` tables, `Chunk.embedding` as a `vector` column. Check: `create_all` runs clean against an empty DB; tables + columns visible via `\d` in psql.
- [ ] **Step 4 — Tenant registration.** Build: `POST /auth/register` creates a `Tenant` + first `User`, returns a JWT. Check: register a new tenant → 201, JWT decodes to the correct `tenant_id` and `user_id`.
- [ ] **Step 5 — Login.** Build: `POST /auth/login` verifies bcrypt password hash, returns a JWT. Check: correct credentials → 200 + valid JWT; wrong password → 401; nonexistent user → 401 (no user enumeration).
- [ ] **Step 6 — Auth dependency + tenant scoping.** Build: `deps.py` extracts `tenant_id`/`user_id` from JWT, injects into request. Check: hitting a protected route without a token → 401; with a token for tenant A, querying tenant B's data → empty result, not another tenant's rows.
- [ ] **Step 7 — Document upload endpoint.** Build: `POST /documents/upload` accepts a file, stores it, creates a `Document` row with `status=pending`. Check: upload a sample PDF → 201, row exists with correct `tenant_id` and `status=pending`, file present in storage.
- [ ] **Step 8 — Background job queue wiring.** Build: ARQ worker connects to Redis, a trivial `ping` job can be enqueued and executed. Check: enqueue `ping` job → worker log shows execution within 1s; `arq` worker survives a Redis restart.
- [ ] **Step 9 — Chunking.** Build: ingestion job splits a `Document`'s text into `Chunk` rows on upload-triggered job. Eval: [Eval-3](#evals) chunking-boundary set must be green before this is done.
- [ ] **Step 10 — Embedding + storage.** Build: each `Chunk` gets an embedding written to its `vector` column via the tenant's configured embedding model. Check: after ingestion, `SELECT embedding FROM chunks WHERE document_id=...` returns non-null vectors of the expected dimension for every chunk.
- [ ] **Step 11 — Retrieval (vector search).** Build: given a query string, return top-k chunks by cosine similarity, scoped to `tenant_id`. Eval: [Eval-4](#evals) retrieval set must hit recall@5 ≥ 0.8 before this is done; tenant isolation re-checked with a cross-tenant query.
- [ ] **Step 12 — Reranking.** Build: local cross-encoder reranks the top-k retrieved chunks before they're passed to the LLM. Eval: [Eval-4](#evals) precision@3 after rerank must beat precision@3 before rerank.
- [ ] **Step 13 — RAG query endpoint (non-streaming).** Build: `POST /query` retrieves, reranks, calls the tenant's LLM (BYOK), returns an answer with source citations. Eval: [Eval-5](#evals) groundedness set must be green before this is done.
- [ ] **Step 14 — Streaming.** Build: `/query` streams tokens via SSE instead of waiting for the full completion. Check: `curl -N` shows tokens arriving incrementally, not all at once; total streamed output matches non-streaming output for the same query.
- [ ] **Step 15 — Shareable tenant endpoint URLs.** Build: each tenant gets a stable public query URL (`/t/{tenant_slug}/query`) usable without the tenant's own JWT (scoped API key instead). Check: hitting the shareable URL with a valid scoped key returns answers scoped to that tenant only; an invalid/expired key → 401.
- [ ] **Step 16 — Team roles.** Build: `Owner`/`Admin`/`Viewer` roles enforced on mutating routes. Check: a `Viewer` hitting `/documents/upload` → 403; an `Owner` can invite/remove users, an `Admin` cannot remove the `Owner`.
- [ ] **Step 17 — Async job failure handling.** Build: ingestion job retries on transient failure, moves to a dead-letter state after N attempts, `Document.status` reflects `failed`. Check: force a job to fail (e.g. bad file) → status becomes `failed` after retries exhaust, not stuck on `pending`.

### Frontend

- [ ] **Step 18 — App skeleton.** Build: React + Tailwind app boots, calls backend `/health`, shows connection status. Check: `npm run dev` → page loads, shows "backend: ok" when backend is running, "backend: down" when it isn't.
- [ ] **Step 19 — Auth screens.** Build: register/login forms call the backend auth endpoints, store JWT client-side. Check: register → redirected to dashboard; login with wrong password → inline error shown, no redirect.
- [ ] **Step 20 — Document upload UI.** Build: drag-and-drop/file-picker upload, shows ingestion status (`pending` → `processing` → `ready`/`failed`) polling or via websocket. Check: upload a file → status visibly transitions through states without a manual page refresh.
- [ ] **Step 21 — Query/chat UI.** Build: chat-style interface hitting `/query` with streaming, renders citations as clickable source links. Check: ask a question → tokens appear incrementally in the UI; clicking a citation shows the source chunk text.
- [ ] **Step 22 — Admin dashboard.** Build: tenant settings (API key management, team members, role assignment) wired to backend endpoints. Check: adding an API key persists and shows masked in the UI; changing a teammate's role reflects immediately on their next request.

### Evals

Its own track, not an afterthought — the harness lands early (Eval-1) and every later retrieval/generation step (Steps 9, 11, 12, 13) plugs a labeled fixture set into it before being marked done.

- [ ] **Eval-1 — Harness.** Build: `eval/` runner loads a fixture set (YAML/JSON), runs it against a target function or endpoint, scores it, writes a run record (score, timestamp, git SHA) to the `eval_runs` table. Check: a trivial fixture set (`1+1=2`-style) runs end-to-end and produces a stored run record.
- [ ] **Eval-2 — Fixture format + seed data.** Build: schema for labeled fixtures (query, expected chunk IDs / expected answer substrings / expected chunk boundaries), seed docs + fixtures checked into `eval/fixtures/`. Check: fixtures load without schema errors; seed docs ingest cleanly in a scratch tenant.
- [ ] **Eval-3 — Chunking-boundary eval.** Build: scores chunk output against 5 hand-labeled docs for sentence/table-split violations. Feeds Step 9. Check: score computed and stored; a deliberately-broken chunker fails the eval (sanity check on the eval itself).
- [ ] **Eval-4 — Retrieval + rerank eval.** Build: scores recall@5 and precision@3 against a 10-query labeled set, run twice (pre-rerank, post-rerank). Feeds Steps 11–12. Check: both scores computed and stored per run; rerank run shows higher precision@3 than pre-rerank run on the same query set.
- [ ] **Eval-5 — Groundedness eval.** Build: scores whether `/query` answers are supported by their cited chunks (substring/entailment check against source text) across a 10-question labeled set. Feeds Step 13. Check: score computed and stored; an answer with a fabricated citation fails the eval.
- [ ] **Eval-6 — Eval runner in CI.** Build: eval suite runs on every backend PR touching `app/pipelines`, `app/models/chunk.py`, or `eval/`; fails the check if any score drops below its threshold. Check: a PR that regresses retrieval recall fails CI; a neutral PR passes.
- [ ] **Eval-7 — Internal eval dashboard (dev-facing UI).** Build: `/evals` page (auth-gated to internal/admin users, not tenant-visible) listing each eval, its latest score, pass/fail, and score trend over time; a "run all" trigger. Check: after a run, the dashboard reflects the new score without a deploy; trend chart shows at least 2 historical points after 2 runs.
- [ ] **Eval-8 — Tenant-facing quality page.** Build: `/dashboard/quality` page in the tenant frontend showing that tenant's own ingestion health and retrieval-confidence signal (not raw eval scores — a simplified trust indicator derived from them). Check: a tenant with 0 failed ingestions sees "healthy"; a tenant with a failed document sees it flagged with a reason.

## Folder structure

```
ragforge/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py            # entrypoint — mounts routers, creates tables
│       ├── core/
│       │   ├── config.py      # settings loaded from .env
│       │   └── security/
│       │       ├── password.py    # bcrypt hash/verify
│       │       ├── jwt.py         # token create/decode
│       │       └── crypto.py      # Fernet encrypt/decrypt for tenant API keys
│       ├── db/
│       │   ├── base.py        # SQLAlchemy declarative base
│       │   └── session.py     # async engine + session factory
│       ├── models/
│       │   ├── tenant.py
│       │   ├── user.py         # scoped by tenant_id, has role
│       │   ├── document.py     # scoped by tenant_id, tracks ingestion status
│       │   └── chunk.py        # scoped by tenant_id, holds the pgvector embedding
│       ├── schemas/
│       │   ├── auth.py
│       │   └── document.py
│       └── api/
│           ├── deps.py         # extracts current tenant from the JWT
│           ├── documents.py    # POST /documents/upload
│           └── auth/
│               ├── register.py # POST /auth/register
│               ├── login.py    # POST /auth/login
│               └── __init__.py # wires both under /auth
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.tsx
│       ├── pages/               # Login, Register, Dashboard, Query, DashboardQuality
│       ├── components/          # ChatWindow, UploadDropzone, CitationLink
│       └── lib/
│           └── api.ts           # typed fetch client for the backend
└── eval/
    ├── runner.py                # loads a fixture set, runs it, scores it, stores the run
    ├── fixtures/
    │   ├── chunking.yaml         # Eval-3 hand-labeled chunk boundaries
    │   ├── retrieval.yaml        # Eval-4 labeled queries + expected chunk IDs
    │   └── groundedness.yaml     # Eval-5 labeled questions + expected answer support
    └── scorers/
        ├── chunking.py
        ├── retrieval.py
        └── groundedness.py
```

Internal eval dashboard lives at `backend/app/api/evals.py` + `frontend/src/pages/EvalsDashboard.tsx` (Eval-7, admin-only). Tenant-facing quality page lives at `frontend/src/pages/DashboardQuality.tsx` (Eval-8, tenant-visible, backed by `backend/app/api/quality.py`).

## Getting started

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Fill in `backend/.env`:

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

Tables are created automatically on startup for now. This is an early-step convenience — before adding new columns in later steps, this project should move to Alembic migrations instead of relying on `create_all`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Points at the backend via `VITE_API_URL` (defaults to `http://localhost:8000`).

### Evals

```bash
cd eval
python runner.py --suite retrieval
python runner.py --suite all
```

Reads fixtures from `eval/fixtures/`, writes run records to the `eval_runs` table — same DB as the backend, so `DATABASE_URL` must be set (reuses `backend/.env`).

## Coding conventions

This project follows a deliberately strict style, applied to every file:

- Max ~20 lines per file or logical section
- One responsibility per file — high modularity over convenience
- A single blank line between every line of code
- Only one-line comments — no docstrings, no block comments
- No unnecessary boilerplate

## API reference (planned)

| Method | Path | Description | Step |
|---|---|---|---|
| GET | `/health` | Liveness check | 1 |
| POST | `/auth/register` | Creates a new tenant + first user, returns a JWT | 4 |
| POST | `/auth/login` | Authenticates an existing user, returns a JWT | 5 |
| POST | `/documents/upload` | Accepts a file, creates a pending document record | 7 |
| POST | `/query` | Retrieves, reranks, and answers with citations (streaming) | 13, 14 |
| POST | `/t/{tenant_slug}/query` | Shareable public query endpoint, scoped API key auth | 15 |
| GET | `/evals` | Internal, admin-only — list evals, latest scores, history | Eval-7 |
| POST | `/evals/run` | Internal, admin-only — trigger an eval run | Eval-7 |
| GET | `/quality` | Tenant-facing — this tenant's ingestion health + retrieval-confidence signal | Eval-8 |

## Known hard problems ahead

Tracked here so they don't get forgotten as we build:

- **Chunking context loss** — naive fixed-size chunking can split a sentence or table across chunks
- **Embedding drift** — swapping embedding models later invalidates existing vectors
- **Tenant data leaks** — app-layer `tenant_id` filtering is the early guardrail; Postgres RLS is the real fix
- **Cold starts** — first query against a tenant's index after inactivity
- **Async job failures** — ingestion jobs need retry/dead-letter handling, not silent failure
- **Context window overflow** — too many retrieved chunks can blow past the LLM's context limit
- **Retrieval confidence illusion** — a high similarity score doesn't guarantee an actually relevant chunk
