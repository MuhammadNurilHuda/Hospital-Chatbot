# Base image
FROM python:3.10-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x ./scripts/entrypoint.sh

# Expose port
EXPOSE 8000

# Set environment vars
ENV PYTHONUNBUFFERED=1

# Entrypoint
ENTRYPOINT ["./scripts/entrypoint.sh"]