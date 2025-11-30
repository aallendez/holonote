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

## Production
Holonote is currently deployed in AWS. For information about deployment and resources used, please visit `infra/` directory in this repo.

- You can **access holonote** through this link http://holonote-frontend-prod.s3-website-eu-west-1.amazonaws.com
    - ⚠️ Warning: make sure the protocol is http (not https). Otherwise the page will not load.

- You can see a snapshot of our **grafana dashboard** through this link https://g-f2a9ab6939.grafana-workspace.eu-west-1.amazonaws.com/dashboard/snapshot/6yMwyfUE1a2Qw5jJbwJR7akGlehNREOf
