#!/bin/sh
uvicorn EntryEndPoint:fastapi_app --reload --host 0.0.0.0 --port=8080 &
gunicorn ExplanationEndPoint:app --reload --bind 0.0.0.0:5000
