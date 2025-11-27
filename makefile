.PHONY: install install-backend install-frontend dev down restart backend frontend test-frontend test-b test-cov-b
install:
	make install-backend
	make install-frontend

install-backend:
	cd backend && pip install -r requirements.txt && cd ..

install-frontend:
	cd frontend && npm install && cd ..

dev:
	docker compose -f docker-compose.dev.yaml up

down:
	docker compose -f docker-compose.dev.yaml down

restart:
	make down
	make dev

backend:
	cd backend && uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

test-f:
	cd frontend && npm run test

test-cov-f:
	cd frontend && npm run test:coverage

test-b:
	cd backend && python -m pytest -q

test-cov-b:
	cd backend && COVERAGE_FILE=/tmp/holonote.coverage python -m pytest --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing

test-cov:
	make test-cov-f
	make test-cov-b

open-f:
	open http://localhost:5173/

open-b:
	open http://localhost:5001/docs#/