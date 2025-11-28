
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
