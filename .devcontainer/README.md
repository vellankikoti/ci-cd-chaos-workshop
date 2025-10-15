# GitHub Codespaces Configuration

This directory contains the configuration files for running the CI/CD Chaos Workshop in GitHub Codespaces.

## Files Overview

- **`devcontainer.json`** - Main dev container configuration
- **`post-create.sh`** - Environment setup script (runs after container creation)
- **`post-start.sh`** - Service initialization script (runs when container starts)
- **`kind-config.yaml`** - Kubernetes cluster configuration for Kind
- **`workshop-launcher.py`** - Interactive workshop launcher
- **`codespaces-setup.sh`** - Additional setup script for Codespaces

## What's Included

### Pre-installed Tools
- Python 3.11 with pip
- Docker with Docker-in-Docker support
- Kubernetes CLI (kubectl)
- Kind (Kubernetes in Docker)
- Helm package manager
- Git and GitHub CLI
- Java 17 (for Jenkins)
- VS Code extensions for Python, Docker, Kubernetes, and YAML

### Pre-installed Python Packages
- testcontainers[all]
- pytest and pytest-cov
- requests, colorama, pyyaml
- kubernetes client
- Database drivers (psycopg2-binary, pymysql, redis, pymongo)
- flask, tabulate, cryptography

### Pre-configured Services
- Kind Kubernetes cluster (3 nodes)
- Jenkins with 146+ plugins
- TestContainers Desktop
- Workshop namespace in Kubernetes

## Usage

### Quick Start
1. Open this repository in GitHub Codespaces
2. Wait for environment setup (2-3 minutes)
3. Run: `python3 .devcontainer/workshop-launcher.py`
4. Follow the interactive menu

### Manual Setup
```bash
# TestContainers
cd testcontainers && python3 setup.py

# Jenkins
cd jenkins && python3 jenkins-setup.py setup

# Kubernetes
cd kubernetes && python3 universal-setup.py
```

## Access Points

- **Jenkins**: http://localhost:8080 (admin/admin)
- **Kubernetes Dashboard**: `kubectl proxy` then http://localhost:8001
- **Workshop Files**: `/workspaces/ci-cd-chaos-workshop/`

## Troubleshooting

### Common Issues
1. **Docker not working**: The environment includes Docker-in-Docker, all commands work normally
2. **Kubernetes issues**: Kind cluster is auto-created, run `kubectl get nodes` to verify
3. **Jenkins not accessible**: Run `python3 jenkins-setup.py status` to check status

### Reset Environment
```bash
python3 .devcontainer/workshop-launcher.py
# Choose option 7 (Cleanup)
```

## Benefits

- ✅ Zero local setup required
- ✅ Consistent environment for all users
- ✅ No network dependency issues
- ✅ All tools pre-installed and configured
- ✅ Interactive guided experience
- ✅ Collaborative features (share Codespace)
- ✅ Free for public repositories

## Compatibility

This Codespaces setup is fully compatible with the existing workshop structure:
- All original setup scripts remain unchanged
- All scenarios and labs work as before
- Local installation still works as alternative
- No breaking changes to existing functionality
