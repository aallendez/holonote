
### Nov 27th, 2025
- I created the main CI pipeline composed of backend, frontend and release.
    - Frontend CI takes care of ensuring frontend code is correct.
    - Backend CI takes care of ensuring backend code is correct.
    - Release CI builds docker images from frontend and backend and stores them in ghcr (github-owned and free).
        It also creates a **tag** (e.g. v1.2.1) for the app if the commit or PR comes with a prefix (feat, fix, etc...).

        This will be useful for setting the value of prod.
- I created a `pre-commit-config.yaml`. This is a pipeline that will run when a commit is made and will run formatting, linting and unit tests of the code. This ensures:

    1. All code pushed to repo is well written.
    2. CI pipelines are executed correctly (no error on CI for backend and frontend).

### Nov 28th, 2025
- I created a small set of simple integration tests.
- I set up the CD pipeline (not working yet).
- I created the initial AWS infra with terraform.

### Nov 29th, 2025
- Spent the day debugging issues between resources (ECS, RDS and frontend in S3)

### Nov 30th, 2025
- Setting up grafana and prometheus monitoring with AWS native resources for initial prototyping. In the future will most likely move to my own setup to reduce prodution costs.
    - This is a snapshot of my grafana dashboard (defined in file `deployment/holonote-backend.json`)
        https://g-f2a9ab6939.grafana-workspace.eu-west-1.amazonaws.com/dashboard/snapshot/D8U0XbUENoxWNoGsukydO4SgzX1ZFhqW
- Setting up the CD pipeline to read the version from infra variables and deploy the builds with said tag.
