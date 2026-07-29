#!/bin/bash
set -e

echo "=== Funding.Wiki Deploy ==="
cd /workspace

echo "--- 1. Git pull ---"
git pull origin master

echo "--- 2. Instal·la dependències Python ---"
pip install -r requirements.txt --quiet

echo "--- 3. Migracions ---"
python manage.py migrate --noinput

echo "--- 4. Build frontend ---"
cd frontend
npm ci --quiet
npm run build
cd ..

echo "--- 5. Copy index.html to the template ---"
cp statfiles/static/vue/index.html templates/vue/index.html

echo "--- 6. Restart Gunicorn ---"
pkill -HUP gunicorn || true
sleep 2
if ! pgrep gunicorn > /dev/null; then
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon
fi

echo "=== Deploy complete ==="
