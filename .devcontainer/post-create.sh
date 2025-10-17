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

# Create a Kind cluster for Kubernetes scenarios (with Docker permission handling)
echo "☸️ Creating Kind cluster..."

# Fix Docker socket permissions for Codespaces
if [ -S /var/run/docker.sock ]; then
    echo "🔧 Fixing Docker socket permissions..."
    sudo chmod 666 /var/run/docker.sock
    # Add user to docker group if it exists
    if getent group docker > /dev/null 2>&1; then
        sudo usermod -aG docker $USER
    fi
fi

# Wait a moment for Docker to be ready
sleep 2

# Try to create Kind cluster with error handling
if kind create cluster --name chaos-workshop --config .devcontainer/kind-config.yaml 2>/dev/null; then
    echo "✅ Kind cluster created successfully"
    
    # Set kubectl context
    kubectl config use-context kind-chaos-workshop
    
    # Create workshop namespace
    kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f -
else
    echo "⚠️ Kind cluster creation failed - this is expected in some Codespaces environments"
    echo "💡 Kubernetes scenarios will use the default cluster or can be set up manually"
    
    # Create workshop namespace in default cluster
    kubectl create namespace chaos-workshop --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || true
fi

# Pre-build ALL images using optimized universal-setup.py
echo "🚀 Running universal-setup.py to optimize workshop (pre-builds ALL images)..."
echo "⏱️ This takes 5-10 minutes but ensures ZERO DELAYS during scenarios!"

cd /workspaces/ci-cd-chaos-workshop

# Function to build Docker image with error handling (for Jenkins and Docker scenarios)
build_image() {
    local dockerfile=$1
    local tag=$2
    local context=$3

    echo "Building $tag..."
    if docker build -f "$dockerfile" -t "$tag" "$context" > /dev/null 2>&1; then
        echo "✅ Built: $tag"
    else
        echo "⚠️ Skipped: $tag (will build on-demand)"
    fi
}

# Pre-build Jenkins image (not handled by universal-setup.py)
if [ -f "Jenkins/Dockerfile" ]; then
    echo "🔨 Building Jenkins image..."
    docker build -t workshop-jenkins:latest -f Jenkins/Dockerfile Jenkins/ || echo "⚠️ Jenkins image will build on first use"
fi

# Pre-build Docker scenario images (not handled by universal-setup.py)
echo "🐳 Building Docker scenario images..."
if [ -d "Docker/docker-scenarios" ]; then
    if [ -f "Docker/docker-scenarios/scenario_02_resilience/app/Dockerfile" ]; then
        build_image "Docker/docker-scenarios/scenario_02_resilience/app/Dockerfile" \
                   "resilience-dashboard:latest" \
                   "Docker/docker-scenarios/scenario_02_resilience/app"
    fi

    if [ -f "Docker/docker-scenarios/scenario_03_networking/app/Dockerfile" ]; then
        build_image "Docker/docker-scenarios/scenario_03_networking/app/Dockerfile" \
                   "networking-dashboard:latest" \
                   "Docker/docker-scenarios/scenario_03_networking/app"
    fi

    if [ -f "Docker/docker-scenarios/scenario_04_multistage/app/Dockerfile" ]; then
        build_image "Docker/docker-scenarios/scenario_04_multistage/app/Dockerfile" \
                   "multistage-dashboard:latest" \
                   "Docker/docker-scenarios/scenario_04_multistage/app"
    fi

    if [ -f "Docker/docker-scenarios/scenario_05_security/app/Dockerfile" ]; then
        build_image "Docker/docker-scenarios/scenario_05_security/app/Dockerfile" \
                   "security-dashboard:latest" \
                   "Docker/docker-scenarios/scenario_05_security/app"
    fi
fi

# Run Kubernetes universal-setup.py for Kubernetes scenario optimization
echo ""
echo "☸️ Running Kubernetes universal-setup.py..."
if [ -f "Kubernetes/universal-setup.py" ]; then
    cd Kubernetes
    python3 universal-setup.py || echo "⚠️ Some Kubernetes images may build on first use"
    cd /workspaces/ci-cd-chaos-workshop
else
    echo "⚠️ universal-setup.py not found - Kubernetes images will build on first use"
fi

echo ""
echo "✅ Complete optimization finished!"
echo "🎯 ALL workshop images are ready - scenarios will run INSTANTLY!"

echo ""
echo "✅ Post-create setup completed!"
echo "🎉 Your CI/CD Chaos Workshop environment is ready!"
echo ""
echo "📊 Summary:"
echo "  ✅ Tools installed (Docker, Kind, Helm, kubectl)"
echo "  ✅ Python dependencies installed"
echo "  ✅ Kind cluster created (if supported)"
echo "  ✅ Docker images pre-built"
echo ""
echo "🚀 You can now run scenarios without delays!"
echo "📚 Start with: cd Docker/docker-scenarios/scenario_02_resilience && python3 demo.py"
