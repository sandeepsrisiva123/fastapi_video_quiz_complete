#!/bin/bash
set -e

# Wait for Postgres to be ready
echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Postgres is up - continuing"

# Run Alembic migrations if alembic.ini exists
if [ -f "alembic.ini" ]; then
  echo "Running migrations..."
  alembic upgrade head || true
fi

# Start FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
