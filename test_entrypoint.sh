#!/bin/bash

echo "Esperando o banco de dados ficar pronto..."

while ! nc -z test-db 5432; do
  sleep 0.1
done

echo "Banco pronto, rodando migrations..."

cd app/
alembic upgrade head
cd ..

export PYTHONPATH=/app

# Executa pytest na pasta de testes
pytest tests --maxfail=1 --disable-warnings -v
