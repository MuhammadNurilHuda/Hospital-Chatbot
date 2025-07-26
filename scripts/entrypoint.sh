#!/bin/sh
# Wait for Postgres
echo "⏳ Menunggu postgres $DB_HOST:$DB_PORT..."
until nc -z $DB_HOST $DB_PORT; do sleep 1; done

# Run migrations / create tables
echo "📦 Menerapkan database migrations..."
python - << 'EOF'
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
EOF

# Start the FastAPI server
echo "🚀 Menjalankan FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info