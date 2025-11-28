# Prompts & Logs

This document aims to track the prompts and logs of the progress I make in this project by myself or with the use of AI.

### Sprint 1

I provide context to AI with project tree with command `tree -L 3 -I "node_modules" -I "__pycache__"`.

**Backend:**
- Help me create a docker-compose file that includes a react remix frontend, a fastapi backend, and a postgres database.
    Also used AI for some troubleshooting in the process.
- Github actions for release were not made with AI. I recycled an action I created during summer since it has the same functionality.
- After an error with a library that env couldn't resolve, I asked cursor to fix it and it changed the `Dockerfile` updating the `RUN` command.

**Frontend:**
- AI helped me during the firebase setup with troubleshooting since I had errors:
    - I had errors with naming .env variables, so I asked AI to help me with the naming since vite only makes available variables with VITE_ prefix.
    - I needed help with the `authContext.tsx` file. AI made it for me. `firebase.ts`, however, was done by me, following firebase documentation.
- Login page: help me create a login page with a google login button and a email/password login form.
- Signup page: help me create a signup page with a email/password signup form.

### Sprint 2

**Backend:**
- Create unit tests for the crud ops in my backend @entries.py and @holos.py. Make it able to execute a test cov with make test-cov-b
- Error handling in api. Asked this to cursor: Add basic error handling to routes in @entries.py and @holos.py
- Used cursor to expand unit tests (prev 70%) to reach 80-90%. Asked: I have ~72% coverage. we need an 80-90% cov. 1. Make more test to reach the % 2. Organize them same as src (folder for api tests, folder for db tests, etc). Don't be too ambicious. Make one test, check it works and how much % we gain, and do that proceduraly until we reach a decent %.

**Frontend:**
- Generate tests for the api in the frontend and include the command to execute them in @makefile as make test-frontend
- Using components, generate a prototype for a dashboard page for holonote. It must have a clean design like modern startups have nowadays.
    It must include:
    - Latest entries
    - Toolbar (create, search entry)
    - Stats (streaks)
    - Github like UI displaying dates with entries where each day is a box
- Generate mock data so I can visualize the GUI with real data. Entries data will come like this: ""Attached example response from the backend""
- I used cursor AI to generate the interface of the Warning popup, loading animation.
- I used cursor AI to help me fix some errors when running frontend tests (Help me fix the error in this frontent test [attached log]).

In a final review of code implementation, I asked AI to sweep the codebase, check for code smells and provide me with a report and action items. Propmt: Read the codebase and look for code smells (specially in backend), make a small report and action items.

Other chats: (these specially include architecture and infra decisions)
- Backend implementation of firebase: https://chatgpt.com/share/68d6c9e8-d1f0-8001-9cc4-0cc8c82b8457
- Frontend API calling implementation: https://chatgpt.com/share/68d821af-66c8-8001-8abc-865431e3658c
