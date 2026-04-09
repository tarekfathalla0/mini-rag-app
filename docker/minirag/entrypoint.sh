#!/bin/bash
set -e

echo "⏳ Waiting for PostgreSQL..."

# استنى لحد ما DB تفتح
while ! nc -z pgvector 5432; do
  sleep 1
done

echo "✅ PostgreSQL is up!"

# safety زيادة
sleep 3

echo "🚀 Running database migrations..."
cd /app/models/db_shcemes/minirag/
alembic upgrade head
cd /app

echo "🔥 Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1