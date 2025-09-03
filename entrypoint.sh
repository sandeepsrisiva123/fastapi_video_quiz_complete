
#!/bin/bash
set -e
echo "Waiting for Postgres..."
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Postgres up"
if [ -f "alembic.ini" ]; then
  alembic upgrade head || true
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
