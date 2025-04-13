#!/bin/bash

# Start FastAPI with Uvicorn and serve frontend via static files
uvicorn backend.main:app --host 0.0.0.0 --port 8000
