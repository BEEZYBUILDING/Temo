#!/bin/sh

echo "Waiting for PostgreSQL..."
until python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    conn.close()
    print('PostgreSQL ready')
except Exception as e:
    exit(1)
"; do
  echo "PostgreSQL not ready yet..."
  sleep 2
done

echo "Running migrations..."
python manage.py migrate

echo "Starting service..."
exec "$@"