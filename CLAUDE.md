# SmartLearn Agent

## Project

SmartLearn Agent is an AI-powered learning assistant that parses PDF lecture slides and answers students' course-related questions with citations.

## Tech Stack

- Backend: Python + FastAPI
- Frontend: React + Vite
- LLM: OpenRouter (`google/gemma-4-26b-a4b-it:free`)
- Vector Search: FAISS (Day 3)

## AI Coding Environment

- Claude Code uses DeepSeek directly through `ANTHROPIC_BASE_URL`.
- Python API exercises use OpenRouter.
- Never route Claude Code through OpenRouter.
- Never put API keys into source code, prompts, logs, or documentation.

## Development Conventions

- Store API keys in `.env` and never commit them.
- Use the project `venv` for Python dependencies.
- Keep changes small and limited to the requested files.
- Before editing, explain the plan and identify affected files.
- After editing Python, run an appropriate syntax check or test.
- Commit messages use `type: description`, such as `feat: add CLI Q&A`.

## Safety Rules

- Do not read, print, modify, or commit `.env`.
- Do not modify or commit `venv/`.
- Do not run destructive commands.
- Do not change dependency lock files unless the task requires it.
- Show the changed files and test results after implementation.

## Do Not Modify

- `.env`
- `venv/`
- `package-lock.json` unless a frontend dependency change is approved
