install:
	cd backend && pip install -r requirements.txt
	pip install -r requirements.txt

dev:
	docker compose up -d
	sleep 2
	open http://localhost:5173/

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d