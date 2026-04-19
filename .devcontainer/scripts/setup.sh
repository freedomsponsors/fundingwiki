#!/bin/bash
set -e

# Host UID often differs from the container user's UID on macOS, which makes git
# flag /workspace as "dubious ownership". Whitelist it for this user's gitconfig.
git config --global --add safe.directory /workspace

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

echo "Creating system users..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='Mai').exists():
    User.objects.create_user(username='Mai', email='mai@localhost', password='mai')
    print('OpenAI user (Mai) created.')
if not User.objects.filter(username='Ana').exists():
    User.objects.create_user(username='Ana', email='ana@localhost', password='ana')
    print('Anonymous user (Ana) created.')
"

echo "Setting up frontend..."
cd frontend
if [ ! -f .env ]; then
  cat > .env <<'ENVEOF'
VITE_LINK_PREFIX=
VITE_API_URL=http://localhost:8000/
VITE_STATIC_URL=http://localhost:8000/
ENVEOF
  echo "Created frontend/.env"
fi
npm install

echo "Setup completo!"
