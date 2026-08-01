# RAGForge Coding Standards

Tool-agnostic reference for anyone (human or AI) contributing to this repo. Applies to `backend/`, `frontend/`, and `eval/`. Overrides any global/personal coding-standards defaults — this file is the source of truth for RAGForge specifically.

## File rules

- Max ~30 lines per file (code lines, not counting blank lines)
- Max ~15 lines per function
- One responsibility per file
- No two files share a filename anywhere in the repo
- No two functions share a name anywhere in the repo
- Shared/reused logic goes in a `utils/` folder local to its layer (`app/core/utils/`, `app/db/utils/`, etc.) — not duplicated across files
- Exactly one comment per file, placed at the top, stating what the file does — no docstrings, no inline comments, no per-function comments

## Naming

- Python: snake_case files and functions, PascalCase classes
- JS/TS: kebab-case files, PascalCase components
- Functions: verb_noun (`get_user`, `create_order`)
- Constants: UPPER_SNAKE_CASE

## Backend (FastAPI)

- Async endpoints, SQLAlchemy async engine
- PostgreSQL + pgvector, Alembic for migrations once past the initial `create_all` convenience phase
- LangChain for RAG orchestration
- **BYOK** — tenants supply their own LLM key (OpenAI / Claude / Gemini / Mistral); never hardcode a single provider
- Type hints on every function signature
- Pydantic models for all request/response bodies
- Every route scoped by `tenant_id` pulled from the JWT via `deps.py` — never trust a client-supplied tenant id
- Specific exception types only, no bare `except`

## Frontend (React + Tailwind)

- Functional components with hooks only, one component per file
- Business logic extracted into custom hooks, not inlined in components
- Typed fetch client (`lib/api.ts`) — no ad-hoc `fetch` calls scattered across components

## Evals

- Every retrieval/generation feature (chunking, retrieval, reranking, groundedness) ships with a labeled fixture set and a scorer before it's considered done — see the Evals track in `README.md`
- Eval runs are stored (score, timestamp, git SHA), not just printed — both the internal dashboard and CI gate read from stored runs, not live output

## Git workflow

- Never push directly to `main`
- Branch naming: `feature/*`, `fix/*`, `refactor/*`, `docs/*`, `test/*`
- Conventional commits: `type(scope): description` (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`)
- Keep commits atomic and focused
- Commit and push as `ushanagallashashank@gmail.com`

## Testing

- pytest for backend, Vitest for frontend
- Write tests for business logic, not framework glue

## Security

- Validate all inputs at the API boundary
- Secrets via environment variables only, never committed
- Tenant API keys Fernet-encrypted before touching the database
- HTTPS required in production
