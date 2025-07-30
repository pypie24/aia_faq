# This repo for implement aia project faq

# How to run
- copy `.env.sample` to `.env` and fill full infomation

## Run with docker
- docker compose up

## Run in locally
- install python3.8 or upper
- run: `python -m venv env`(to create a virtual environment)
- run: `pip install -r requirements.txt`(to install library)
- run: `pre-commit install`(to init pre-commit)
- run: `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`

# Migration
- run: `alembic update head` before start app
- run: `alembic upgrade head` to migrate revision
- Create at revision to apply models database
  + Add models at src/models
  + import models in `src/models/__init__.py`
  + run: `alembic revision --autogenerate -m "message here"

## Commit
- run: `pre-commit install`
- run: `pre-commit run --all-files`
- run: `git add .`
- run: `git commit -m "message"`
- run: `git push origin main`
