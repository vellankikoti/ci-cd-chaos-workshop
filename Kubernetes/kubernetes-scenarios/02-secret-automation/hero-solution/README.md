# 🔐 Secure Todo App - Secret Management Demo

**Clean, Simple, Powerful!**

A complete demonstration of Kubernetes secret management using a secure Todo application.

## What's Included

- **app.py** - Flask-based Todo application with security features
- **deploy.py** - One-command deployment script with auto-generated secrets
- **Dockerfile** - Secure container definition (non-root user)
- **k8s-manifests.yaml** - Complete Kubernetes configuration
- **requirements.txt** - Python dependencies

## Quick Start

```bash
# One command to deploy everything:
python3 deploy.py
```

That's it! The script will:
1. Generate cryptographically secure secrets (32 chars)
2. Build Docker image
3. Deploy to Kubernetes
4. Show you how to access the app

## What You'll See

The deployment script provides **copy-paste ready commands**:

```
🔧 PORT-FORWARD COMMANDS (Copy & Paste):
   kubectl port-forward -n secure-todo svc/secure-todo-app 31005:80

🔐 SECURITY FEATURES:
   ✅ Auto-generated 32-char secure passwords
   ✅ Secrets encrypted in etcd
   ✅ Non-root container (UID 1000)
   ✅ Read-only root filesystem
   ✅ Dropped all capabilities
   ✅ Resource limits
   ✅ Health checks

🧪 TEST SECURITY:
   kubectl get secret app-secrets -n secure-todo -o yaml
   kubectl get secret app-secrets -n secure-todo -o jsonpath='{.data.api-key}' | base64 -d
```

## Access the App

**Option 1:** NodePort (if available)
```bash
http://localhost:31005
```

**Option 2:** Port-forward (works everywhere)
```bash
kubectl port-forward -n secure-todo svc/secure-todo-app 31005:80
# Then open: http://localhost:31005
```

## Features

### Security
- Kubernetes Secrets for sensitive data
- Non-root container (UID 1000)
- Read-only root filesystem
- No privileged escalation
- All capabilities dropped
- Resource limits enforced

### Application
- Beautiful gradient UI
- Create, complete, delete tasks
- Real-time statistics
- Auto-refresh every 3 seconds
- SQLite database (simple, no external deps)

### Deployment
- Auto-generated secrets (cryptographically secure)
- Environment detection (Minikube/Docker Desktop)
- Health checks included
- Clear, actionable output

## Verify Deployment

```bash
# Check all resources
kubectl get all -n secure-todo

# View secrets
kubectl get secrets -n secure-todo

# Check logs
kubectl logs -n secure-todo -l app=secure-todo-app

# Test health endpoint
curl http://localhost:31005/health
```

## Cleanup

```bash
kubectl delete namespace secure-todo
```

## Architecture

```
┌─────────────────────────────────────┐
│  Kubernetes Cluster                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Namespace: secure-todo      │   │
│  │                             │   │
│  │  ┌──────────────────────┐   │   │
│  │  │ Secret: app-secrets  │   │   │
│  │  │  - api-key           │   │   │
│  │  │  - app-secret        │   │   │
│  │  └──────────────────────┘   │   │
│  │            ↓                │   │
│  │  ┌──────────────────────┐   │   │
│  │  │ Deployment: secure-todo-app │   │   │
│  │  │  Replicas: 2         │   │   │
│  │  │  Port: 8080          │   │   │
│  │  │  User: 1000 (non-root)  │   │
│  │  └──────────────────────┘   │   │
│  │            ↓                │   │
│  │  ┌──────────────────────┐   │   │
│  │  │ Service: secure-todo-app    │   │   │
│  │  │  Type: NodePort      │   │   │
│  │  │  Port: 31005         │   │   │
│  │  └──────────────────────┘   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Learning Objectives

After completing this scenario, you'll understand:
1. How to generate secure secrets programmatically
2. How to use Kubernetes Secrets to pass sensitive data
3. How to configure security contexts for containers
4. How to implement health checks
5. How to set resource limits
6. How to verify secret encryption at rest

## Pro Tips

- **Secrets are base64 encoded, not encrypted in transit** - Use TLS for production
- **Secret rotation** - In production, implement automated secret rotation
- **RBAC** - Limit which pods can access which secrets
- **External Secret Management** - Consider HashiCorp Vault or AWS Secrets Manager for production
