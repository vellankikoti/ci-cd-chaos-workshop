# 🚀 Docker Scenario 02 — Progressive Chaos Engineering Workshop

**Goal:**  
- Demonstrate powerful Docker capabilities in chaos engineering  
- Show progressive chaos engineering with 5 different failure scenarios
- Run chaos tests to simulate failures and prove system resilience  
- Teach how to run Docker **inside** Docker (DinD) safely
- Provide educational, interactive experience with real microservices
- **Enhanced learning experience** with real microservices, interactive debugging, and comprehensive monitoring

This scenario creates an unforgettable learning experience:

> **Progressive Chaos Engineering: From Broken to Production-Ready with Real Microservices**

---

# 🚀 Quick Start

## Local Demo (Recommended for Presentations)

1. **Clone and navigate to the scenario:**
   ```bash
   cd Docker/docker-scenarios/scenario_02_chaos_pipeline
   ```

2. **Run the manual demo (step-by-step control):**
   ```bash
   ./demo_manual.sh
   ```
   This script allows you to control the pace and explain each step.

3. **Run the simple demo (automated):**
   ```bash
   ./demo_simple.sh
   ```
   This script runs automatically without user interaction.

## Demo Scripts Explained

- **`demo_manual.sh`**: Step-by-step control with educational pauses
- **`demo_simple.sh`**: Automated demo for quick demonstrations
- **`cleanup.sh`**: Clean up all containers and resources

## Progressive Chaos Scenarios

The demo supports multiple scenarios:

- **`progressive-demo`**: Complete educational journey (recommended)
- **`chaos-full`**: Maximum chaos (everything broken)
- **`chaos-free`**: Perfect pipeline (all working)
- **`chaos-1/2/3`**: Progressive fixes showing issue cascades

---

# ✅ Prerequisites

- Docker installed
- Basic Python knowledge
- Enough RAM (~2GB) for Docker containers
- **NEW:** `jq` for JSON formatting (will be auto-installed if missing)

---

# ✅ Enhanced Scenario Overview

In this **enhanced** scenario:

✅ We run progressive chaos engineering with **real microservices**:
  - **Step 1**: Network failure simulation with web API
  - **Step 2**: Resource limitation with image processing service
  - **Step 3**: Service dependency failure with Redis session management
  - **Step 4**: Database connection failure with MySQL user management
  - **Step 5**: Success! Complete resilient microservices architecture

✅ **NEW:** Each step provides:
- **Real microservices** with actual functionality
- **Interactive debugging endpoints** (`/health`, `/debug`, `/metrics`)
- **Comprehensive health monitoring** and observability
- **Educational insights** and learning objectives
- **Progressive complexity** and hands-on learning
- **Production-ready patterns** and best practices

✅ **NEW:** Enhanced learning experience:
- **Real web APIs** that participants can interact with
- **Comprehensive monitoring** with health checks and metrics
- **Debugging tools** for troubleshooting
- **Educational content** explaining what's happening
- **Production-ready features** like fallback mechanisms

✅ Entire environment runs in Docker:
- No external services required
- 100% self-contained chaos engineering
- Real-world failure simulation with real microservices

---

# ✅ Enhanced Directory Structure

Your workshop directory will look like this:

```
scenario_02_chaos_pipeline/
│
├── scenarios/
│     ├── step1_fail_network/
│     │   ├── app.py          # NEW: Real web API with network testing
│     │   └── Dockerfile      # NEW: Enhanced with Flask and monitoring
│     ├── step2_fail_resource/
│     │   ├── app.py          # NEW: Image processing service with memory limits
│     │   └── Dockerfile      # NEW: Enhanced with numpy, PIL, psutil
│     ├── step3_fail_service/
│     │   ├── app.py          # NEW: Session management with Redis
│     │   └── Dockerfile      # NEW: Enhanced with Redis integration
│     ├── step4_fail_db/
│     │   ├── app.py          # NEW: User management with MySQL
│     │   └── Dockerfile      # NEW: Enhanced with SQLAlchemy
│     └── step5_success/
│         ├── app.py          # NEW: Complete resilient microservices
│         └── Dockerfile      # NEW: Production-ready with all dependencies
│
├── tests/
│     └── test_mysql.py
│
├── setup.sh
├── cleanup.sh
├── test_setup.sh
├── test_all_scenarios.sh
├── demo_manual.sh           # Step-by-step demo script
├── demo_simple.sh           # Automated demo script
└── README.md
```

---

# ✅ Enhanced Progressive Chaos Engineering Steps

## 🎯 Learning Objectives

This **enhanced** scenario teaches chaos engineering through 5 progressive steps with **real microservices**:

### **Step 1: Network Failure** 🌐
- **What happens**: Web API tries to connect to external services and internal dependencies
- **Learning**: Network connectivity issues in containers with real API testing
- **Real Service**: Web API with network diagnostics and health monitoring
- **Educational value**: Understanding container networking limitations with hands-on debugging

### **Step 2: Resource Failure** 💾
- **What happens**: Image processing service runs with memory constraints
- **Learning**: Resource constraints and container limits with real image processing
- **Real Service**: Image processing microservice with memory monitoring
- **Educational value**: Understanding Docker resource management with actual workloads

### **Step 3: Service Failure** 🔌
- **What happens**: Session management service tries to connect to Redis (not running)
- **Learning**: Service dependencies and microservices with real session management
- **Real Service**: Session management microservice with Redis integration
- **Educational value**: Understanding service discovery and dependencies with real use case

### **Step 4: Database Failure** 🗄️
- **What happens**: User management service tries to connect to MySQL (not running)
- **Learning**: Database connectivity and persistence with real user management
- **Real Service**: User management microservice with MySQL integration
- **Educational value**: Understanding database dependencies with actual user operations

### **Step 5: Success!** 🎉
- **What happens**: Complete resilient microservices architecture with all dependencies
- **Learning**: Production-ready, resilient system with comprehensive monitoring
- **Real Service**: Complete microservices architecture with health monitoring, metrics, and observability
- **Educational value**: Understanding what makes a system production-ready and resilient

---

# ✅ Enhanced Step-by-Step Implementation

---

## ✅ 1. Enhanced Progressive Chaos Engineering Apps

Each scenario step now has **real microservices** with actual functionality:

### **Step 1: Network Failure** (`scenarios/step1_fail_network/app.py`)

**NEW:** Real web API with network testing capabilities:

```python
# Enhanced with Flask web API, network diagnostics, health monitoring
# Real endpoints: /health, /debug, /run-experiment
# Educational content and debugging tools
```

**Educational Value**: Shows how containers handle network connectivity issues with real API testing.

### **Step 2: Resource Failure** (`scenarios/step2_fail_resource/app.py`)

**NEW:** Real image processing service with memory monitoring:

```python
# Enhanced with image processing, memory monitoring, resource diagnostics
# Real endpoints: /health, /debug, /process-image/<w>/<h>, /run-experiment
# Educational content and resource debugging tools
```

**Educational Value**: Demonstrates Docker resource limits and memory management with actual workloads.

### **Step 3: Service Failure** (`scenarios/step3_fail_service/app.py`)

**NEW:** Real session management service with Redis integration:

```python
# Enhanced with session management, Redis integration, service diagnostics
# Real endpoints: /health, /debug, /session/create, /session/<id>, /run-experiment
# Educational content and service debugging tools
```

**Educational Value**: Shows service dependencies and microservices architecture with real session management.

### **Step 4: Database Failure** (`scenarios/step4_fail_db/app.py`)

**NEW:** Real user management service with MySQL integration:

```python
# Enhanced with user management, MySQL integration, database diagnostics
# Real endpoints: /health, /debug, /user/create, /user/<id>, /run-experiment
# Educational content and database debugging tools
```

**Educational Value**: Demonstrates database connectivity and persistence with actual user operations.

### **Step 5: Success!** (`scenarios/step5_success/app.py`)

**NEW:** Complete resilient microservices architecture:

```python
# Enhanced with comprehensive monitoring, metrics, observability
# Real endpoints: /health, /debug, /metrics, /run-experiment
# Production-ready features and best practices
```

**Educational Value**: Shows what a production-ready, resilient system looks like with comprehensive monitoring.

---

## ✅ 2. Enhanced Dockerfiles

Each step now has enhanced Dockerfiles with proper dependencies:

### **Step 1 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 2 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask numpy pillow psutil
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 3 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask redis
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 4 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask sqlalchemy pymysql
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 5 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask redis sqlalchemy pymysql psutil requests
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

---

## ✅ 5. Enhanced Demo Scripts

**NEW:** `demo_manual.sh` and `demo_simple.sh` - Comprehensive demo scripts with:

- **Real microservices** with actual functionality
- **Interactive debugging** and health monitoring
- **Educational content** and learning objectives
- **Progressive complexity** and hands-on learning
- **Production-ready features** and best practices

### **Run the Enhanced Demo**

```bash
# Make the scripts executable
chmod +x demo_manual.sh demo_simple.sh

# Run the manual demo (step-by-step control)
./demo_manual.sh

# Or run the simple demo (automated)
./demo_simple.sh
```

This will:
- Build all enhanced scenario containers
- Start each service with proper configuration
- Run chaos experiments with real microservices
- Show health monitoring and debugging information
- Provide educational insights and learning objectives
- Demonstrate progressive complexity and resilience

---

## ✅ 6. Enhanced Automation and Testing Scripts

### **Setup Scripts**

- **`setup.sh`**: Complete environment setup with Docker
- **`cleanup.sh`**: Clean up all containers and images
- **`test_setup.sh`**: Verify environment is working correctly

### **Testing Scripts**

- **`test_all_scenarios.sh`**: Run all 5 enhanced scenarios locally for testing
- **`test_setup.sh`**: Verify the complete setup is working
- **`demo_manual.sh`**: Step-by-step demo with real microservices
- **`demo_simple.sh`**: Automated demo with real microservices

### **Local Testing**

Run all enhanced scenarios locally to verify they work:

```bash
# Step-by-step demo (recommended for presentations)
./demo_manual.sh

# Automated demo (for quick testing)
./demo_simple.sh
```

This will:
- Build all enhanced scenario Docker images
- Run each scenario with real microservices
- Show expected failures and success with educational content
- Provide interactive debugging and health monitoring
- Demonstrate progressive complexity and learning

---

## ✅ 7. Run the Enhanced Demo

1. **Setup the environment:**
   ```bash
   ./setup.sh
   ```

2. **Run the demo:**
   ```bash
   # For presentations with step-by-step control
   ./demo_manual.sh
   
   # For automated testing
   ./demo_simple.sh
   ```

3. **Watch Enhanced Chaos Unfold:**
   - Each step demonstrates different failure modes with **real microservices**
   - Interactive debugging and health monitoring
   - Educational content and learning objectives
   - Progressive complexity and resilience building

4. **Clean up when done:**
   ```bash
   ./cleanup.sh
   ```

---

## ✅ 8. Educational Value

This enhanced scenario provides:

### **Real Microservices**
- **Step 1**: Network testing with real web API
- **Step 2**: Image processing with memory monitoring
- **Step 3**: Session management with Redis integration
- **Step 4**: User management with MySQL database
- **Step 5**: Complete resilient microservices architecture

### **Interactive Learning**
- Health monitoring and debugging endpoints
- Educational content and learning objectives
- Progressive complexity and hands-on experience
- Production-ready patterns and best practices

### **Comprehensive Monitoring**
- Health checks and metrics
- Debugging tools and observability
- Error handling and fallback mechanisms
- Performance monitoring and resource management

---

## ✅ 9. Troubleshooting

### **Common Issues**

1. **Port conflicts**: Make sure ports 8081-8085 are available
2. **Memory issues**: Ensure you have at least 2GB RAM available
3. **Docker permissions**: Make sure your user can run Docker commands
4. **Network issues**: Check if Docker networking is working properly

### **Debugging**

- Use `docker logs <container-name>` to check container logs
- Use `docker ps` to see running containers
- Use `docker stats` to monitor resource usage
- Check the `/health` and `/debug` endpoints for each service

### **Cleanup**

If something goes wrong, clean up everything:

```bash
./cleanup.sh
```

This will remove all containers, images, and networks created by the demo.

---

## ✅ 10. Next Steps

After completing this scenario, you can:

1. **Explore the code**: Look at the `scenarios/` directory to understand how each service works
2. **Modify scenarios**: Add your own chaos experiments or failure modes
3. **Extend the demo**: Add more services or complexity to the scenarios
4. **Practice chaos engineering**: Use this as a foundation for your own chaos engineering practices

---

## 🎯 Summary

This enhanced scenario provides:

✅ **Real microservices** with actual functionality  
✅ **Interactive debugging** and health monitoring  
✅ **Educational content** and learning objectives  
✅ **Progressive complexity** and hands-on learning  
✅ **Production-ready features** and best practices  
✅ **Comprehensive monitoring** and observability  

**Perfect for**: Workshops, presentations, learning Docker, and understanding chaos engineering with real microservices!

