#!/bin/bash

echo "🧹 Cleaning up all chaos-app-v* containers..."
docker ps -a --filter "name=chaos-app-v" -q | xargs -r docker rm -f
echo "✅ All chaos-app-v* containers removed." 