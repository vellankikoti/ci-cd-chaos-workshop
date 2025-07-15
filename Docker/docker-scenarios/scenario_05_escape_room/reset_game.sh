#!/bin/bash

echo "🐛 Resetting Dr. Bug's Chaos Laboratory..."

# Stop and remove any existing containers
echo "🧹 Cleaning up existing containers..."
docker rm -f network-spy memory-victim secret-keeper 2>/dev/null || true

# Remove the suspicious image
echo "🗑️ Removing suspicious image..."
docker rmi suspicious-image 2>/dev/null || true

# Restart the web app
echo "🔄 Restarting the escape room..."
docker-compose restart

# Wait for the app to start
echo "⏳ Waiting for app to start..."
sleep 5

# Trigger setup
echo "🔧 Setting up all puzzles..."
curl -s http://localhost:5000/test_setup > /dev/null

echo "✅ Reset complete! Open http://localhost:5000 to start fresh!"
echo "🎯 All puzzles are ready for the workshop!" 