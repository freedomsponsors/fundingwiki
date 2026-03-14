#!/bin/bash
set -e

# Django dev server
python manage.py runserver 0.0.0.0:8000 &

# Vite dev server
cd frontend && npm run dev -- --host 0.0.0.0 &

wait
