#!/bin/bash
set -e

echo "🚀 GitHub Codespaces CI/CD Chaos Workshop Setup"
echo "=============================================="

# Make scripts executable
chmod +x .devcontainer/post-create.sh
chmod +x .devcontainer/post-start.sh
chmod +x .devcontainer/workshop-launcher.py

# Set up environment variables
export WORKSPACE_DIR="/workspaces/ci-cd-chaos-workshop"
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Create a welcome message
cat > /workspaces/ci-cd-chaos-workshop/WELCOME.md << 'EOF'
# 🚀 Welcome to CI/CD Chaos Workshop!

This workshop runs entirely in GitHub Codespaces - no local setup required!

## Quick Start

1. **Run the workshop launcher:**
   ```bash
   python3 .devcontainer/workshop-launcher.py
   ```

2. **Or start with specific phases:**
   ```bash
   # TestContainers
   cd testcontainers && python3 setup.py
   
   # Jenkins
   cd jenkins && python3 jenkins-setup.py setup
   
   # Kubernetes
   cd kubernetes && python3 universal-setup.py
   ```

## What's Included

- ✅ Python 3.11 with all dependencies
- ✅ Docker with Docker-in-Docker support
- ✅ Kubernetes cluster (Kind)
- ✅ Jenkins with all plugins
- ✅ TestContainers Desktop
- ✅ All workshop scenarios and labs

## Access Points

- **Jenkins:** http://localhost:8080 (admin/admin)
- **Kubernetes Dashboard:** `kubectl proxy` then http://localhost:8001
- **Workshop Files:** All in `/workspaces/ci-cd-chaos-workshop/`

## Need Help?

- Check the README.md files in each directory
- Run `python3 .devcontainer/workshop-launcher.py` for interactive menu
- All setup scripts are in `.devcontainer/`

Happy learning! 🎉
EOF

echo "✅ Codespaces setup completed!"
echo "🎯 Run 'python3 .devcontainer/workshop-launcher.py' to start!"
