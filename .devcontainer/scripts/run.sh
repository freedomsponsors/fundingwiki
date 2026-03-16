#!/bin/bash
set -e

trap 'kill 0' EXIT

# Django dev server
python manage.py runserver 0.0.0.0:8000 &

# Vite dev server
cd frontend && npm run dev -- --host 0.0.0.0 &

wait
