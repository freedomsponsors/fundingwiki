#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "import psycopg; psycopg.connect('host=db dbname=djangology user=djangology password=djangology')" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL is ready."

echo "Running migrations..."
python manage.py migrate

echo "Loading language data..."
python manage.py fillLanguageData || true

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username=__import__('os').environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
        email=__import__('os').environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@localhost'),
        password=__import__('os').environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin'),
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

echo "Installing frontend dependencies..."
cd frontend && npm install

echo "Setup completo!"
