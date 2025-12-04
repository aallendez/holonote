# Holonote

### See video demo of Holonote in production [HERE](https://drive.google.com/file/d/1IYXYzSCMF0AjAMfJWIUSeictsQgkJAQj/view?usp=sharing)


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

Activate pre-commit hooks
```bash
pre-commit install
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

You can access a report of frontend and backend unit test coverage as well as integration tests by checking the `documentation/test_results.txt` file.

## Production
Holonote is currently deployed in AWS. For information about deployment and resources used, please visit `infra/` directory in this repo.

- You can **access holonote** through this link http://holonote-frontend-prod.s3-website-eu-west-1.amazonaws.com
    - ⚠️ Warning: make sure the protocol is http (not https). Otherwise the page will not load.

⚠️ Warning: due to costs grafana is not currently active. If you want to see grafana logs, please execute:
```bash
terraform apply
```
This will produce the outputs you see below.

### Terraform outputs:
```bash
alb_dns = "holonote-alb-1922459695.eu-west-1.elb.amazonaws.com"

amp_workspace_id = "ws-95928c16-b299-49c9-8d4a-445be879d34f"

db_endpoint = "holonotedb.cpag0wewiohh.eu-west-1.rds.amazonaws.com"

ecs_cluster_id = "arn:aws:ecs:eu-west-1:774305601984:cluster/holonote-cluster"

frontend_url = "http://holonote-frontend-prod.s3-website-eu-west-1.amazonaws.com"

github_actions_role_arn = "arn:aws:iam::774305601984:role/holonote-ci-deploy-role"

grafana_endpoint = "g-f2a9ab6939.grafana-workspace.eu-west-1.amazonaws.com"

grafana_workspace_id = "g-f2a9ab6939"
```
