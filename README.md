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

If you want to deploy holonote using your own AWS account, you can do so by running the following command:
```bash
make deploy
```
This will deploy the application to your own AWS account using Terraform.

You can access the application through the URL provided by the output of the command.
