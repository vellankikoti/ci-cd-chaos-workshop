# 🚀 Docker Scenario 02 — Progressive Chaos Engineering Pipeline

**Goal:**  
- Demonstrate progressive chaos engineering through real microservices
- Show how systems fail and recover at different levels
- Teach resilience patterns with hands-on failure simulation
- Provide an educational, interactive chaos engineering experience

This scenario demonstrates:

> **Progressive Chaos Engineering: From Network Failures to Production Success**

---

# ✅ Prerequisites

- Docker installed
- Docker Compose installed
- Basic Python knowledge
- ~4GB RAM for multiple containers
- curl (for testing endpoints)

---

# ✅ Scenario Overview

This scenario demonstrates **progressive chaos engineering** through 5 stages:

1. **Step 1: Network Failures** - Simulate network connectivity issues
2. **Step 2: Resource Failures** - Demonstrate memory exhaustion and OOM kills
3. **Step 3: Service Failures** - Show service degradation and timeouts
4. **Step 4: Database Failures** - Simulate database connectivity issues
5. **Step 5: Production Success** - Real microservices with Redis and MySQL

Each step includes:
- Real microservices with monitoring endpoints
- Educational failure demonstrations
- Interactive debugging capabilities
- Comprehensive health checks

---

# ✅ Directory Structure

```
scenario_02_chaos_pipeline/
│
├── scenarios/
│   ├── step1_fail_network/
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── step2_fail_resource/
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── step3_fail_service/
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── step4_fail_db/
│   │   ├── app.py
│   │   └── Dockerfile
│   └── step5_success/
│       ├── app.py
│       ├── Dockerfile
│       └── docker-compose.yml
│
├── demo_manual.sh          # Interactive step-by-step demo
├── demo_simple.sh          # Automated demo
├── cleanup.sh              # Cleanup script
├── setup.sh               # Setup script
└── DEMONSTRATION_GUIDE.md # Detailed demo guide
```

---

# ✅ Quick Start

## 🚀 Run the Interactive Demo

```bash
cd Docker/docker-scenarios/scenario_02_chaos_pipeline

# Run the interactive demo (recommended)
./demo_manual.sh

# Or run the automated demo
./demo_simple.sh
```

## 🧹 Cleanup

```bash
./cleanup.sh
```

---

# ✅ Demo Scripts Overview

## 📋 Manual Demo (`demo_manual.sh`)

**Perfect for presentations and teaching:**

- **Step-by-step control** - You control the pace
- **Educational explanations** - Each step is explained
- **Interactive endpoints** - Show real monitoring data
- **Failure demonstrations** - Controlled chaos experiments
- **Success demonstration** - Real production system

**Features:**
- ✅ Progressive failure simulation
- ✅ Real microservices with monitoring
- ✅ Educational content and explanations
- ✅ Interactive debugging endpoints
- ✅ Production-ready step 5 with Redis/MySQL

## 🤖 Simple Demo (`demo_simple.sh`)

**Perfect for automated testing:**

- **Fully automated** - Runs all steps automatically
- **Quick validation** - Verify everything works
- **CI/CD ready** - Can be integrated into pipelines

---

# ✅ Step-by-Step Breakdown

---

## 🔴 Step 1: Network Failures

**Port:** 8081  
**Focus:** Network connectivity issues

**What happens:**
- Simulates network timeouts and connectivity issues
- Demonstrates how applications handle network failures
- Shows monitoring and debugging capabilities

**Key endpoints:**
- `http://localhost:8081/health` - Health status
- `http://localhost:8081/debug` - Network diagnostics
- `http://localhost:8081/run-experiment` - Network failure simulation

---

## 🔴 Step 2: Resource Failures

**Port:** 8082  
**Focus:** Memory exhaustion and OOM kills

**What happens:**
- Demonstrates memory exhaustion scenarios
- Shows OOM killer behavior
- Educational experiments before full failure

**Key endpoints:**
- `http://localhost:8082/health` - Resource monitoring
- `http://localhost:8082/debug` - System resource info
- `http://localhost:8082/run-experiment` - Memory experiments

**Educational approach:**
1. Safe experiments first
2. Gradual memory pressure
3. Full OOM demonstration last

---

## 🔴 Step 3: Service Failures

**Port:** 8083  
**Focus:** Service degradation and timeouts

**What happens:**
- Simulates service unresponsiveness
- Demonstrates timeout handling
- Shows service monitoring capabilities

**Key endpoints:**
- `http://localhost:8083/health` - Service health
- `http://localhost:8083/debug` - Service diagnostics
- `http://localhost:8083/run-experiment` - Service failure simulation

---

## 🔴 Step 4: Database Failures

**Port:** 8084  
**Focus:** Database connectivity issues

**What happens:**
- Simulates database connection failures
- Demonstrates graceful degradation
- Shows database monitoring

**Key endpoints:**
- `http://localhost:8084/health` - Database health
- `http://localhost:8084/debug` - Database diagnostics
- `http://localhost:8084/run-experiment` - Database failure simulation
- `http://localhost:8084/create-user` - User management

---

## 🟢 Step 5: Production Success

**Port:** 8085  
**Focus:** Real microservices with resilience

**What happens:**
- Real Redis and MySQL services
- Production-ready monitoring
- Comprehensive health checks
- All services working together

**Services:**
- **App:** Flask microservice on port 8085
- **Redis:** Session management on port 6379
- **MySQL:** Database on port 3306

**Key endpoints:**
- `http://localhost:8085/health` - Complete system health
- `http://localhost:8085/debug` - System diagnostics
- `http://localhost:8085/metrics` - Performance metrics
- `http://localhost:8085/run-experiment` - Success experiments
- `http://localhost:8085/create-user` - User management

---

# ✅ Educational Value

## 🎓 Learning Objectives

✅ **Chaos Engineering Principles:**
- Progressive failure simulation
- Controlled chaos experiments
- Real-world failure scenarios

✅ **Microservices Architecture:**
- Service communication patterns
- Health check implementations
- Monitoring and observability

✅ **Docker & Containerization:**
- Multi-container applications
- Service orchestration
- Resource management

✅ **Resilience Patterns:**
- Graceful degradation
- Circuit breaker patterns
- Failure recovery strategies

## 🔍 Key Concepts Demonstrated

1. **Network Resilience** - How apps handle network issues
2. **Resource Management** - Memory limits and OOM handling
3. **Service Reliability** - Timeout and degradation patterns
4. **Database Resilience** - Connection failure handling
5. **Production Readiness** - Real services working together

---

# ✅ Advanced Features

## 📊 Monitoring & Observability

Each step includes comprehensive monitoring:

- **Health Checks** - Real-time system status
- **Debug Endpoints** - Detailed diagnostics
- **Metrics** - Performance data
- **Experiments** - Controlled failure simulation

## 🔧 Technical Implementation

- **Flask Microservices** - Lightweight, fast
- **Docker Compose** - Service orchestration
- **Health Checks** - Built-in monitoring
- **Error Handling** - Graceful failure modes
- **Logging** - Comprehensive debugging

## 🎯 Educational Design

- **Progressive Complexity** - Each step builds on the previous
- **Real Failures** - Actual system failures, not simulations
- **Interactive Learning** - Hands-on experimentation
- **Production Reality** - Real microservices architecture

---

# ✅ Troubleshooting

## 🚨 Common Issues

**Port conflicts:**
```bash
# Check what's using a port
lsof -i :8081

# Clean up containers
./cleanup.sh
```

**Memory issues:**
```bash
# Check Docker memory usage
docker system df

# Clean up Docker
docker system prune -a
```

**Service not starting:**
```bash
# Check container logs
docker logs <container_name>

# Rebuild containers
docker-compose down && docker-compose up --build
```

## 🔧 Debug Commands

     ```bash
# Check all running containers
docker ps

# Check container logs
docker logs <container_name>

# Test health endpoints
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8083/health
curl http://localhost:8084/health
curl http://localhost:8085/health
```

---

# ✅ What This Proves

✅ **Chaos Engineering Works:**
- Progressive failure simulation
- Real-world failure scenarios
- Educational value

✅ **Microservices Resilience:**
- Service isolation
- Graceful degradation
- Health monitoring

✅ **Docker Power:**
- Multi-container orchestration
- Resource management
- Service communication

✅ **Production Readiness:**
- Real services working together
- Comprehensive monitoring
- Resilience patterns

---

# 🚀 Running Everything

## Quick Start

```bash
cd Docker/docker-scenarios/scenario_02_chaos_pipeline

# Interactive demo (recommended)
./demo_manual.sh

# Automated demo
./demo_simple.sh

# Cleanup
./cleanup.sh
```

## Manual Step-by-Step

```bash
# Step 1: Network failures
cd scenarios/step1_fail_network
docker build -t chaos-step1 .
docker run -d -p 8081:5000 --name chaos-step1 chaos-step1

# Step 2: Resource failures
cd ../step2_fail_resource
docker build -t chaos-step2 .
docker run -d -p 8082:5000 --name chaos-step2 chaos-step2

# Step 3: Service failures
cd ../step3_fail_service
docker build -t chaos-step3 .
docker run -d -p 8083:5000 --name chaos-step3 chaos-step3

# Step 4: Database failures
cd ../step4_fail_db
docker build -t chaos-step4 .
docker run -d -p 8084:5000 --name chaos-step4 chaos-step4

# Step 5: Production success
cd ../step5_success
docker-compose up -d --build
```

---

# 🎯 Success Criteria

✅ **Educational Value:** Participants understand chaos engineering principles

✅ **Technical Demonstration:** Real microservices with actual failures

✅ **Interactive Experience:** Hands-on experimentation and learning

✅ **Production Reality:** Real services working together successfully

✅ **Comprehensive Coverage:** Network, resource, service, database, and success scenarios

This scenario provides a complete, educational chaos engineering experience that teaches real-world resilience patterns through hands-on experimentation.
