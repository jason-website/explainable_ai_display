#!/bin/sh
gunicorn ExplanationEndPoint:app --reload --bind 0.0.0.0:5000 --log-level critical
uvicorn EntryEndPoint:app --reload --host 0.0.0.0 --port=5001 --no-access-log --log-level=critical

