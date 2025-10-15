#!/bin/bash
set -e

echo "🚀 Setting up CI/CD Chaos Workshop environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install additional tools
echo "🔧 Installing additional tools..."
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

# Install Kind (Kubernetes in Docker)
echo "☸️ Installing Kind..."
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Install Helm
echo "🎯 Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Testcontainers Desktop (headless mode)
echo "🧪 Setting up Testcontainers..."
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

# Create a Kind cluster for Kubernetes scenarios
echo "☸️ Creating Kind cluster..."
kind create cluster --name chaos-workshop --config .devcontainer/kind-config.yaml

# Set kubectl context
kubectl config use-context kind-chaos-workshop

# Create workshop namespace
kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Post-create setup completed!"
echo "🎉 Your CI/CD Chaos Workshop environment is ready!"
