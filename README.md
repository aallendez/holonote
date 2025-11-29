# Holonote


## Local Development

Before you run this app, make sure you have installed npm, python, and docker desktop.

### 0. Requirements

- Python Version equal or higher to 3.11

### 1. Install dependencies

Create virtual env
```bash
cd backend && python -m venv .venv
```
Enter virtual env
```bash
source .venv/bin/activate && cd ..
```

Install backend and frontend dependencies
```bash
make install
```
Build your application
```bash
make dev
```


### Stop & Restart
To stop or restart this app, run:
Stope the app
```bash
make down
```
Restart the app
```bash
make restart
```

### Test Coverage
To run test coverage on both backend and frontend, run:
```bash
make test-cov
```
Backend
```bash
make test-cov-b
```
Frontend
```bash
make test-cov-f
```
Integration (Backend)
```bash
make integration
```
