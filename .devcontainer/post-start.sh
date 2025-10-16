#!/bin/bash
set -e

echo "🚀 Starting CI/CD Chaos Workshop services..."

# Fix Docker socket permissions for Codespaces
if [ -S /var/run/docker.sock ]; then
    echo "🔧 Ensuring Docker socket permissions..."
    sudo chmod 666 /var/run/docker.sock 2>/dev/null || true
    # Add user to docker group if it exists
    if getent group docker > /dev/null 2>&1; then
        sudo usermod -aG docker $USER 2>/dev/null || true
    fi
fi

# Ensure Docker is running (if systemctl is available)
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl start docker 2>/dev/null || true
    sudo systemctl enable docker 2>/dev/null || true
fi

# Check if Kind cluster exists and is running
if kind get clusters 2>/dev/null | grep -q "chaos-workshop"; then
    echo "✅ Kind cluster already exists"
    kubectl config use-context kind-chaos-workshop 2>/dev/null || true
else
    echo "☸️ Creating Kind cluster..."
    if kind create cluster --name chaos-workshop --config .devcontainer/kind-config.yaml 2>/dev/null; then
        echo "✅ Kind cluster created successfully"
        kubectl config use-context kind-chaos-workshop
    else
        echo "⚠️ Kind cluster creation failed - using default cluster"
        echo "💡 Kubernetes scenarios will work with the default cluster"
    fi
fi

# Verify cluster is running
echo "🔍 Verifying cluster status..."
if kubectl get nodes >/dev/null 2>&1; then
    kubectl get nodes
    echo "✅ Kubernetes cluster is accessible"
else
    echo "⚠️ Kubernetes cluster not accessible - some scenarios may not work"
fi

# Create workshop namespace if it doesn't exist
kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || true

# Set default namespace
kubectl config set-context --current --namespace=chaos-workshop 2>/dev/null || true

echo "✅ All services started successfully!"
echo "🎯 Ready to start the workshop!"
