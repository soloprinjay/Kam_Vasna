#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 0.5
done

echo "PostgreSQL started"

# Run migrations and collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
