# Scenario 04: Docker Image Scanner - Hands-On, Production-Grade Guide

## 🎯 Learning Objective
Master Docker security analysis using real vulnerability scanning (Trivy via Docker). Learn to identify security issues, apply best practices, and make informed image choices through interactive, unforgettable demos.

---

## 📋 Prerequisites
- Docker installed and running (no need to install Trivy locally)
- Web browser
- Basic Docker knowledge

---

## 🚀 Quick Start

### 1. No Trivy Installation Needed!
The app uses the official Trivy Docker image (`aquasec/trivy:latest`). Just ensure Docker is running and the Docker socket is available.

### 2. Start the Analyzer
```bash
python app.py
```

### 3. Open the App
- Go to: http://localhost:8000

---

## ✅ Pre-Flight Checklist
- [ ] Docker is running (`docker ps`)
- [ ] Port 8000 is available
- [ ] Internet access (for pulling images and Trivy Docker image)

---

## 🐳 Demo Images
- `nginx:1.25-alpine` (secure, minimal)
- `python:3.11-slim` (modern, secure)
- `python:3.8` (older, more vulnerabilities)
- `node:18-alpine` (modern Node.js)
- `ubuntu:22.04` (large, more vulnerabilities)

---

## 🛠️ How to Use

### A. Image Analysis
1. Enter an image name (e.g., `nginx:1.25-alpine`)
2. Click "Analyze Image"
3. Review:
   - Security score & vulnerability breakdown
   - Best practices & educational insights
   - Industry comparison

### B. Image Comparison (Supercharged!)
1. Click the "Compare Images" tab
2. Enter two image names (e.g., `python:3.8` vs `python:3.11-slim`)
3. See:
   - Animated, side-by-side comparison
   - Winner highlighted with a trophy
   - Mini bar charts for vulnerabilities & score
   - Downloadable comparison report
   - Fun facts & security tips
   - Swap or reset for more comparisons

---

## 🧠 What You'll Learn
- CVE understanding & severity
- Attack surface minimization
- Secure base image selection
- Non-root user best practices
- Multi-stage builds & layer optimization
- Secret management & image scanning
- Real-world CI/CD integration
- How to compare images for security trade-offs

---

## 🧹 Clean Up
```bash
# Stop the app (Ctrl+C)
# Optionally, clean up uploads/
rm -rf uploads/*
```

---

## 💡 Next Steps
- Integrate scanning into your CI/CD pipeline
- Apply best practices to your own Dockerfiles
- Educate your team on container security
- Stay updated with the latest security tools

---

**Built by Koti with ❤️ for this workshop.** 