#!/bin/bash

echo "Esperando o banco de dados ficar pronto..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Banco pronto, rodando migrations..."

alembic upgrade head

exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-config utils/logging.yml --reload
