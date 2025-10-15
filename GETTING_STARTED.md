# 🚀 Getting Started Guide

## Quick Start (2 minutes)

### Option 1: GitHub Codespaces (Recommended)
1. **Click this button**: [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?repo=vellankikoti/ci-cd-chaos-workshop)
2. **Wait 2-3 minutes** for environment setup
3. **Run this command**:
   ```bash
   python3 .devcontainer/workshop-launcher.py
   ```
4. **Choose your adventure** from the menu!

### Option 2: Local Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
   cd ci-cd-chaos-workshop
   ```
2. **Run setup scripts**:
   ```bash
   python3 testcontainers/setup.py
   python3 jenkins/jenkins-setup.py setup
   python3 kubernetes/universal-setup.py
   ```
3. **Start the workshop**:
   ```bash
   python3 .devcontainer/workshop-launcher.py
   ```

## What You'll Need

### For Codespaces
- ✅ **Nothing!** Everything is pre-installed
- ✅ **Just a browser** - Works on any device

### For Local Installation
- ✅ **Python 3.10+** - [Install Python](https://python.org/downloads/)
- ✅ **Docker Desktop** - [Install Docker](https://docker.com/products/docker-desktop/)
- ✅ **Kubernetes** - [Install Kubernetes](https://kubernetes.io/docs/setup/)

## Workshop Phases

### Phase 1: 🧪 TestContainers Chaos (15-35 min)
**Learn**: Real database testing with PostgreSQL, MySQL, Redis, MongoDB
```bash
cd testcontainers
python3 setup.py
python3 labs/basics/lab1_postgresql_basics.py
```

### Phase 2: 🐳 Docker Sabotage (35-55 min)
**Learn**: Multi-stage builds, security, networking, optimization
```bash
cd docker/docker-scenarios
# Follow individual scenario guides
```

### Phase 3: 🤖 Jenkins Pipeline Showdown (55-80 min)
**Learn**: CI/CD automation, pipeline as code, integration testing
```bash
cd jenkins
python3 jenkins-setup.py setup
# Access: http://localhost:8080 (admin/admin)
```

### Phase 4: ☸️ Kubernetes Warzone (80-105 min)
**Learn**: Container orchestration, deployments, scaling, GitOps
```bash
cd kubernetes
python3 universal-setup.py
kubectl get nodes
```

## Common Commands

### Check Status
```bash
# Jenkins
python3 jenkins-setup.py status

# Kubernetes
kubectl get nodes

# Docker
docker ps
```

### Reset Environment
```bash
python3 .devcontainer/workshop-launcher.py
# Choose option 7 (Cleanup)
```

### Get Help
```bash
python3 .devcontainer/workshop-launcher.py
# Choose option 6 (Documentation)
```

## Access Points

- **Jenkins**: http://localhost:8080 (admin/admin)
- **Kubernetes Dashboard**: `kubectl proxy` → http://localhost:8001
- **Workshop Files**: `/workspaces/ci-cd-chaos-workshop/` (Codespaces)

## Troubleshooting

### Codespaces Issues
- **Not starting?** Check [GitHub Codespaces status](https://github.com/codespaces)
- **Docker not working?** It's pre-configured, all commands work normally
- **Kubernetes issues?** Kind cluster is auto-created, run `kubectl get nodes`

### Local Installation Issues
- **Python issues?** Ensure Python 3.10+ is installed and in PATH
- **Docker issues?** Start Docker Desktop and ensure it's running
- **Kubernetes issues?** Check your cluster is running with `kubectl get nodes`

## Need More Help?

- **📚 Full Documentation**: See [README.md](README.md)
- **🎮 Interactive Help**: Run the workshop launcher and choose option 6
- **💬 Community**: Join discussions in the repository issues
- **📧 Contact**: [vellankikoti@gmail.com](mailto:vellankikoti@gmail.com)

---

**🎉 Ready to become a DevOps hero? Let's get started!**
