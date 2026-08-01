# root command entrypoints wrapping backend, frontend, and eval workflows

ifeq ($(OS),Windows_NT)
PYTHON ?= python
BACKEND_VENV_PYTHON := .venv/Scripts/python.exe
BACKEND_VENV_PIP := .venv/Scripts/pip.exe
BACKEND_VENV_UVICORN := .venv/Scripts/uvicorn.exe
BACKEND_VENV_PYTHON_ROOT := backend/.venv/Scripts/python.exe
else
PYTHON ?= python3
BACKEND_VENV_PYTHON := .venv/bin/python
BACKEND_VENV_PIP := .venv/bin/pip
BACKEND_VENV_UVICORN := .venv/bin/uvicorn
BACKEND_VENV_PYTHON_ROOT := backend/.venv/bin/python
endif

.PHONY: install install-backend install-frontend run-backend run-frontend eval health

install: install-backend install-frontend

install-backend:
	cd backend && $(PYTHON) -m venv .venv && $(BACKEND_VENV_PYTHON) -m pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

run-backend:
	cd backend && $(BACKEND_VENV_UVICORN) app.main:app --reload --reload-dir app

run-frontend:
	cd frontend && npm run dev

eval:
	cd eval && ../$(BACKEND_VENV_PYTHON_ROOT) runner.py --suite all

health:
	curl -s localhost:8000/health
