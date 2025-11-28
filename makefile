.PHONY: install install-backend install-frontend dev down restart backend frontend test-frontend test-b test-cov-b format-check format

help:
	@echo "Available make commands:"
	@grep -E '^[a-zA-Z0-9_-]+:' $(MAKEFILE_LIST) | cut -d: -f1 | grep -v '^\.' | sort -u | awk '{print " - "$$0}'

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

test-f:
	cd frontend && npm run test

test-cov-f:
	cd frontend && npm run test:coverage

test-b:
	cd backend && python -m pytest -q

integration:
	python -m pytest backend/tests/integration

test-cov-b:
	cd backend && COVERAGE_FILE=/tmp/holonote.coverage python -m pytest --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing

test-cov:
	make test-cov-f
	make test-cov-b

format-check:
	@if [ -d "backend" ]; then \
		cd backend && \
		if [ -f ".venv/bin/python" ]; then \
			.venv/bin/python -m black --check src tests; \
		else \
			python -m black --check src tests; \
		fi; \
	else \
		if [ -f ".venv/bin/python" ]; then \
			.venv/bin/python -m black --check src tests; \
		else \
			python -m black --check src tests; \
		fi; \
	fi

format:
	@if [ -d "backend" ]; then \
		cd backend && \
		if [ -f ".venv/bin/python" ]; then \
			.venv/bin/python -m black src tests; \
		else \
			python -m black src tests; \
		fi; \
	else \
		if [ -f ".venv/bin/python" ]; then \
			.venv/bin/python -m black src tests; \
		else \
			python -m black src tests; \
		fi; \
	fi

commit:
	pre-commit run --all-files
