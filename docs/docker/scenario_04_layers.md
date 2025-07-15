# 🚀 Scenario 04: Docker Image Scanner

---

## 🎯 Scenario Goal

**Mission:**
Empower learners to master Docker image security using real vulnerability scanning (Trivy via Docker). Learn to:

✅ Analyze images for vulnerabilities and best practices
✅ Compare images side-by-side for security trade-offs
✅ Make informed, production-grade image choices
✅ Experience a modern, interactive, and unforgettable demo

---

## 📝 High-Level Concept

You'll use a web-based tool (no CLI required!) to:
- Analyze any public Docker image for vulnerabilities, security score, and best practices
- Instantly compare two images with animated, side-by-side results
- Download reports and get actionable security tips
- All powered by Trivy running in Docker (no local install needed)

---

## 🚦 Quick Start

1. Ensure Docker is running (no need to install Trivy)
2. Start the analyzer:
   ```bash
   python app.py
   ```
3. Open your browser to [http://localhost:8000](http://localhost:8000)

---

## 🧪 Demo Flow

### A. Analyze an Image
- Enter an image name (e.g., `nginx:1.25-alpine`)
- Click "Analyze Image"
- Review vulnerabilities, security score, and best practices

### B. Compare Images
- Click the "Compare Images" tab
- Enter two image names (e.g., `python:3.8` vs `python:3.11-slim`)
- See animated, side-by-side results with winner, bar charts, and tips
- Download the comparison report or swap images for more fun

---

## 💡 What You'll Learn
- How to spot and fix real CVEs
- Why base image choice matters
- Best practices for secure Dockerfiles
- How to integrate scanning into CI/CD

---

## 🧹 Clean Up
```bash
# Stop the app (Ctrl+C)
# Optionally, clean up uploads/
rm -rf uploads/*
```

---

**Built by Koti with ❤️ for this workshop.**

