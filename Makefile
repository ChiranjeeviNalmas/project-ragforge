# root command entrypoints wrapping backend, frontend, and eval workflows

.PHONY: install install-backend install-frontend run-backend run-frontend eval health

install: install-backend install-frontend

install-backend:
	cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

run-backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --reload-dir app

run-frontend:
	cd frontend && npm run dev

eval:
	cd eval && ../backend/.venv/bin/python runner.py --suite all

health:
	curl -s localhost:8000/health
