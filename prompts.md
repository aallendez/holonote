# Prompts & Logs

This document aims to track the prompts and logs of the progress I make in this project by myself or with the use of AI.

### Sprint 1

I provide context to AI with project tree with command `tree -L 3 -I "node_modules" -I "__pycache__"`.

** Backend **
- Help me create a docker-compose file that includes a react remix frontend, a fastapi backend, and a postgres database.
    Also used AI for some troubleshooting in the process.
- Github actions for release were not made with AI. I recycled an action I created during summer since it has the same functionality.

** Frontend **
- AI helped me during the firebase setup with troubleshooting since I had errors:
    - I had errors with naming .env variables, so I asked AI to help me with the naming since vite only makes available variables with VITE_ prefix.
    - I needed help with the `authContext.tsx` file. AI made it for me. `firebase.ts`, however, was done by me, following firebase documentation.
- Login page: help me create a login page with a google login button and a email/password login form.
- Signup page: help me create a signup page with a email/password signup form.

Other chats:
- Backend implementation of firebase: https://chatgpt.com/share/68d6c9e8-d1f0-8001-9cc4-0cc8c82b8457