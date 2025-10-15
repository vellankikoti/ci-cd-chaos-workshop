#!/bin/bash
set -e

echo "🚀 Starting CI/CD Chaos Workshop services..."

# Ensure Docker is running
sudo systemctl start docker
sudo systemctl enable docker

# Start Kind cluster if not running
if ! kind get clusters | grep -q "chaos-workshop"; then
    echo "☸️ Starting Kind cluster..."
    kind create cluster --name chaos-workshop --config .devcontainer/kind-config.yaml
fi

# Set kubectl context
kubectl config use-context kind-chaos-workshop

# Verify cluster is running
echo "🔍 Verifying cluster status..."
kubectl get nodes

# Create workshop namespace if it doesn't exist
kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f -

# Set default namespace
kubectl config set-context --current --namespace=chaos-workshop

echo "✅ All services started successfully!"
echo "🎯 Ready to start the workshop!"
