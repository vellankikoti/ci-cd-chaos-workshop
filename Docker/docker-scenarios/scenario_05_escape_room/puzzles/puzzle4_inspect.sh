#!/bin/bash

# Puzzle 4: The Secret Hunter
# Dr. NullPointer has hidden a secret environment variable

echo "🔍 Setting up Puzzle 4: The Secret Hunter"
echo "Dr. NullPointer is hiding secrets in a container..."

# Clean up any existing container
docker rm -f secret-keeper 2>/dev/null || true

# Create a container with environment variables containing secrets
docker run -d --name secret-keeper \
  -e SECRET_CODE=docker_master_2025 \
  -e DATABASE_URL=postgres://user:pass@db:5432/app \
  -e API_KEY=sk-1234567890abcdef \
  -e DEBUG=false \
  -e NODE_ENV=production \
  busybox sh -c "
echo 'Container with secrets is running...'
echo 'Use docker inspect to find the SECRET_CODE environment variable'
sleep infinity
"

echo "✅ Puzzle 4 setup complete!"
echo "📝 Container 'secret-keeper' is running with hidden environment variables"
echo "💡 Use: docker inspect secret-keeper | grep -A 10 -B 5 SECRET_CODE"
echo "💡 Find the value of SECRET_CODE and submit it" 