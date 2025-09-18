

backend-dev:
	uvicorn backend.main:app --reload

backend:
	uvicorn backend.main:app

frontend-dev:
	npm run dev

frontend:
	npm run build
	npm run start

frontend-build:
	npm run build