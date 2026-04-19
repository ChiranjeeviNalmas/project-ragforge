install:  # run this first time to set up everything
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

dev:  # start the server with auto-reload for development
	.venv/bin/uvicorn main:app --reload

prod:  # start the server without reload for production
	.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080

cleanup:  # delete all Gemini file search stores and GCS files
	PYTHONPATH=. .venv/bin/python scripts/cleanup.py
