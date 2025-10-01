# Holonote


### Local Development

Before you run this app, make sure you have installed npm, python, and docker desktop.

1. Install dependencies
```bash
cd backend
python -m venv .venv # Create a virtual environment
source .venv/bin/activate # Enter the virtual environment
cd ..
```
```bash
make install # Install backend and frontend dependencies
make dev # Build your application
```

2. Access frontend and backend
```bash
make open-f # Open frontend on browser
make open-b # Open backend on browser
````

3. Logs (if needed). Need to be in separate terminals.
```bash
make logs-f # Frontend logs
make logs-b # Backend logs
```

To stop or restart this app, run:
```bash
make down # stop the app
make restart # restart the app
```

To run test coverage on both backend and frontend, run:
```bash
make test-cov
```

