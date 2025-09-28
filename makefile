.PHONY: install install-backend install-frontend dev down restart backend frontend
install:
	make install-backend
	make install-frontend

install-backend:
	cd backend && pip install -r requirements.txt && cd ..

install-frontend:
	cd frontend && npm install && cd ..

dev:
	docker compose up -d

down:
	docker compose down

restart:
	make down
	make dev

backend:
	cd backend && uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

logs-f:
	docker compose logs -f frontend

logs-b:
	docker compose logs -f backend

open-f:
	open http://localhost:5173/

open-b:
	open http://localhost:5001/docs#/