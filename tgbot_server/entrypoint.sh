#!/bin/bash

echo "Ожидание PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "Запуск Alembic миграций..."
alembic upgrade head

echo "Запуск приложения..."
exec "$@"
