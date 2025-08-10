#!/bin/sh
echo "Waiting for user $POSTGRES_USER and postgres database..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"
