#!/bin/bash
set -e

echo "🚀 Codespaces Fallback Setup"
echo "============================="

# This script provides an alternative setup when Docker-in-Docker has issues

echo "🔧 Setting up fallback environment..."

# Install additional tools that might be missing
echo "📦 Installing additional tools..."
sudo apt-get update -y
sudo apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    jq \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install kubectl if not available
if ! command -v kubectl &> /dev/null; then
    echo "☸️ Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
fi

# Install Helm
echo "🎯 Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install TestContainers
echo "🧪 Setting up TestContainers..."
pip3 install testcontainers[all] --upgrade

# Install additional Python packages
echo "🐍 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install \
    pytest \
    pytest-cov \
    requests \
    colorama \
    pyyaml \
    kubernetes \
    psycopg2-binary \
    pymysql \
    redis \
    pymongo \
    flask \
    tabulate \
    cryptography

# Create workspace directories
echo "📁 Creating workspace directories..."
mkdir -p /workspaces/ci-cd-chaos-workshop/{testcontainers,jenkins,kubernetes,docker}
cd /workspaces/ci-cd-chaos-workshop

# Set up Git configuration
echo "⚙️ Configuring Git..."
git config --global user.name "Workshop User"
git config --global user.email "workshop@example.com"
git config --global init.defaultBranch main

# Create a simple Kubernetes context for testing
echo "☸️ Setting up Kubernetes context..."
kubectl config set-context codespaces --cluster=minikube --user=minikube 2>/dev/null || true
kubectl config use-context codespaces 2>/dev/null || true

# Create workshop namespace
kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || true

echo "✅ Fallback setup completed!"
echo "🎉 Your CI/CD Chaos Workshop environment is ready!"
echo ""
echo "💡 Note: Some Kubernetes scenarios may require a cloud cluster"
echo "   or local Docker Desktop installation for full functionality."
