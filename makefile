install:
	make install-backend
	make install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev:
	docker compose up -d
	sleep 2
	open http://localhost:5173/

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d