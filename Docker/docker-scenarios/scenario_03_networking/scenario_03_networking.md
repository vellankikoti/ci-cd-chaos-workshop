# 🚀 Docker Scenario 03 — Networking Magic: Lifetime Experience

**Goal:**  
- Experience real-world Docker networking problems and their solutions
- See how container communication works (and fails!) in practice
- Learn to debug, fix, and understand containerized apps
- Create a memorable "AHA!" moment about networks and container isolation

This scenario demonstrates:

> **Docker Networking Magic: From Isolation to Communication**

---

# ✅ Prerequisites

- Docker installed
- Basic understanding of containers
- curl (for testing endpoints)
- ~1GB RAM for containers

---

# ✅ Scenario Overview

This scenario creates an unforgettable **AHA moment** by demonstrating:

1. **App Without Database** - Shows what happens when containers can't communicate
2. **Wrong Network** - Demonstrates Docker network isolation
3. **Network Fix** - Reveals the magic of proper container networking
4. **Internal Communication** - Shows container-to-container communication without host access
5. **Network Inspection** - Learn to debug and understand Docker networks
6. **Network Isolation** - Demonstrate security boundaries between networks
7. **Port Publishing** - Understand how to access containers from the host

Each step includes:
- Real failure scenarios with actual error messages
- Educational explanations of what went wrong
- Step-by-step fixes that work
- Interactive testing and validation
- Comprehensive troubleshooting and debugging

---

# ✅ Directory Structure

```
scenario_03_networking/
│
├── app/
│   ├── app.py              # Flask voting application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container definition
├── scripts/
│   ├── run_app_without_db.sh
│   ├── run_app_with_db_wrong_network.sh
│   ├── fix_network.sh
│   ├── run_app_and_redis_no_publish.sh
│   ├── run_isolated_networks.sh
│   ├── run_app_with_port_publish.sh
│   └── cleanup.sh
├── demo_manual.sh         # Interactive step-by-step demo
├── demo_simple.sh         # Automated demo
├── README.md             # Quick start guide
└── scenario_03_networking.md
```

---

# ✅ Quick Start

## 🚀 Run the Interactive Demo (Recommended)

```bash
cd Docker/docker-scenarios/scenario_03_networking

# Run the interactive demo with explanations
./demo_manual.sh

# Or run the automated demo
./demo_simple.sh
```

## 🧹 Cleanup

```bash
./scripts/cleanup.sh
```

---

# ✅ Demo Scripts Overview

## 📋 Manual Demo (`demo_manual.sh`)

**Perfect for presentations and teaching:**

- **Step-by-step control** - You control the pace
- **Educational explanations** - Each step is explained
- **Port checking** - Validates port availability
- **Failure demonstrations** - Shows real error scenarios
- **Success validation** - Confirms fixes work
- **Interactive testing** - Tests voting functionality

**Features:**
- ✅ Port availability checking
- ✅ Container status monitoring
- ✅ Network connectivity testing
- ✅ Educational content and explanations
- ✅ Comprehensive error handling

## 🤖 Simple Demo (`demo_simple.sh`)

**Perfect for automated testing:**

- **Fully automated** - Runs all steps automatically
- **Quick validation** - Verify everything works
- **CI/CD ready** - Can be integrated into pipelines
- **No user interaction** - Perfect for testing

---

# ✅ Step-by-Step Execution

---

## 🔴 Step 1: App Without Database (Expected Failure)

**What happens:**
- Flask voting app starts successfully
- App tries to connect to Redis database
- Redis doesn't exist → connection fails
- Voting crashes with error message

**Learning moment:**
- Containers are isolated by default
- Apps need explicit database connections
- No automatic service discovery

**Key endpoints:**
- `http://localhost:5000` - Voting app (crashes on vote)

---

## 🔴 Step 2: Database in Wrong Network (Expected Failure)

**What happens:**
- Redis database starts successfully
- App tries to connect to Redis by hostname
- Containers in different networks can't communicate
- Hostname resolution fails

**Learning moment:**
- Docker networks isolate containers
- Containers in different networks can't see each other
- Need explicit network configuration

**Key endpoints:**
- `http://localhost:5000` - Voting app (still crashes)

---

## 🟢 Step 3: Fix the Network (Success!)

**What happens:**
- Create custom Docker network
- Put both containers in same network
- Hostname resolution works
- Voting functionality works perfectly

**Learning moment:**
- Custom networks enable container communication
- Hostname resolution within same network
- This is how microservices communicate
- Real-world pattern used daily

**Key endpoints:**
- `http://localhost:5000` - Voting app (works perfectly!)

---

## 🔍 Step 4: Container-to-Container Communication (No Port Publishing)

**What happens:**
- App and Redis run on same network
- Port is NOT published to host
- App is NOT accessible from browser
- But containers can communicate internally

**Learning moment:**
- Containers can communicate without host access
- Port publishing is separate from internal networking
- Useful for internal-only services

**Key endpoints:**
- `http://localhost:5000` - NOT accessible (as expected)

---

## 🔍 Step 5: Network Inspection

**What happens:**
- Use `docker network ls` to see all networks
- Use `docker network inspect` to see container connectivity
- View IP addresses and network details

**Learning moment:**
- Docker networks are powerful tools for organizing and securing container communication
- Network inspection helps debug connectivity issues
- Understanding network topology is crucial for troubleshooting

**Commands to try:**
- `docker network ls` - List all networks
- `docker network inspect vote-net` - Inspect specific network

---

## 🔴 Step 6: Network Isolation (Expected Failure)

**What happens:**
- App and Redis run on different networks
- Both containers are running
- App cannot connect to Redis
- Demonstrates network security boundaries

**Learning moment:**
- Containers on different networks are isolated from each other
- This is a key security feature in Docker
- Network isolation prevents unauthorized communication

**Key endpoints:**
- `http://localhost:5000` - App accessible but fails to connect to Redis

---

## 🟢 Step 7: Port Publishing (Success!)

**What happens:**
- App runs with port published to host
- App is accessible from your computer
- Demonstrates how to access container services from host

**Learning moment:**
- Port publishing (`-p 5000:5000`) lets you access services running in containers from your own machine
- Without port publishing, the app would only be accessible inside Docker

**Key endpoints:**
- `http://localhost:5000` - App accessible from host

---

# ✅ Educational Value

## 🎓 Learning Objectives

✅ **Docker Networking Concepts:**
- Container isolation and communication
- Network types and configurations
- Hostname resolution in Docker
- Port publishing and host access
- Network inspection and debugging

✅ **Real-World Problem Solving:**
- Debugging container connectivity issues
- Understanding error messages
- Step-by-step troubleshooting
- Network inspection and analysis

✅ **Microservices Patterns:**
- Service-to-service communication
- Database connectivity patterns
- Network architecture decisions
- Internal vs external service access

✅ **DevOps Practices:**
- Container orchestration
- Service discovery
- Network security and isolation
- Debugging and monitoring

## 🔍 Key Concepts Demonstrated

1. **Container Isolation** - Why containers can't always talk to each other
2. **Docker Networks** - How to connect containers properly
3. **Hostname Resolution** - How containers find each other
4. **Service Communication** - Real-world microservices patterns
5. **Port Publishing** - How to access containers from the host
6. **Network Inspection** - How to debug and understand Docker networks
7. **Network Isolation** - Security boundaries between containers

---

# ✅ Advanced Features

## 📊 Monitoring & Validation

Each step includes comprehensive validation:

- **Port Checking** - Ensures ports are available
- **Container Status** - Monitors container health
- **Network Testing** - Validates connectivity
- **Voting Tests** - Confirms functionality
- **Error Handling** - Graceful failure modes
- **Network Inspection** - Debug and understand connectivity

## 🔧 Technical Implementation

- **Flask Application** - Lightweight, fast voting app
- **Redis Database** - In-memory data storage
- **Docker Networks** - Custom network configuration
- **Health Checks** - Built-in monitoring
- **Error Handling** - Graceful failure modes
- **Network Debugging** - Comprehensive troubleshooting tools

## 🎯 Educational Design

- **Progressive Complexity** - Each step builds on the previous
- **Real Failures** - Actual system failures, not simulations
- **Interactive Learning** - Hands-on experimentation
- **Production Reality** - Real-world patterns and practices
- **Comprehensive Debugging** - Learn to troubleshoot like a pro

---

# ✅ Troubleshooting & Debugging

## 🚨 Common Issues

**Port conflicts:**
```bash
# Check what's using a port
lsof -i :5000

# Clean up containers
./scripts/cleanup.sh
```

**Container not starting:**
```bash
# Check container logs
docker logs vote-app

# Check container status
docker ps -a
```

**Network issues:**
```bash
# Check network status
docker network ls

# Inspect network
docker network inspect vote-net
```

## 🔧 Debug Commands

```bash
# Check all running containers
docker ps

# Check container logs
docker logs vote-app
docker logs redis-server

# Test app endpoint
curl http://localhost:5000

# Test voting
curl -X POST -d "vote=wfh" http://localhost:5000

# Check network connectivity
docker exec vote-app ping redis-server

# Inspect networks
docker network ls
docker network inspect vote-net

# Get shell inside container
docker exec -it vote-app /bin/sh
```

---

# ✅ What This Proves

✅ **Docker Networking Works:**
- Container isolation and communication
- Real-world failure scenarios
- Step-by-step problem solving
- Network inspection and debugging

✅ **Educational Value:**
- Hands-on learning experience
- Real error messages and fixes
- Production-ready patterns
- Comprehensive troubleshooting skills

✅ **DevOps Skills:**
- Container debugging
- Network troubleshooting
- Service orchestration
- Network security understanding

✅ **Real-World Application:**
- Microservices communication
- Database connectivity
- Network architecture design
- Security and isolation practices

---

# 🚀 Running Everything

## Quick Start

```bash
cd Docker/docker-scenarios/scenario_03_networking

# Interactive demo (recommended)
./demo_manual.sh

# Automated demo
./demo_simple.sh

# Cleanup
./scripts/cleanup.sh
```

## Manual Step-by-Step

```bash
# Step 1: App without database
./scripts/run_app_without_db.sh

# Step 2: Database in wrong network
./scripts/run_app_with_db_wrong_network.sh

# Step 3: Fix the network
./scripts/fix_network.sh

# Step 4: Internal communication (no port publishing)
./scripts/run_app_and_redis_no_publish.sh

# Step 5: Network inspection
docker network ls
docker network inspect vote-net

# Step 6: Network isolation
./scripts/run_isolated_networks.sh

# Step 7: Port publishing
./scripts/run_app_with_port_publish.sh
```

## Individual Commands

```bash
# Build the app
docker build -t vote-app ./app

# Run without database
docker run -d --name vote-app -p 5000:5000 vote-app

# Add Redis in wrong network
docker run -d --name redis-server redis:alpine
docker run -d --name vote-app -p 5000:5000 -e REDIS_HOST=redis-server vote-app

# Fix with custom network
docker network create vote-net
docker run -d --name redis-server --network vote-net redis:alpine
docker run -d --name vote-app --network vote-net -p 5000:5000 -e REDIS_HOST=redis-server vote-app

# Internal communication (no port publishing)
docker run -d --name vote-app --network vote-net -e REDIS_HOST=redis-server vote-app

# Network isolation
docker network create vote-net1
docker network create vote-net2
docker run -d --name redis-server --network vote-net1 redis:alpine
docker run -d --name vote-app --network vote-net2 -p 5000:5000 -e REDIS_HOST=redis-server vote-app
```

---

# 🎯 Success Criteria

✅ **Educational Value:** Participants understand Docker networking concepts comprehensively

✅ **Technical Demonstration:** Real container communication, failures, and debugging

✅ **Interactive Experience:** Hands-on experimentation and learning

✅ **Real-World Application:** Production-ready patterns and practices

✅ **Comprehensive Coverage:** Isolation, communication, inspection, and security

✅ **Debugging Skills:** Network inspection and troubleshooting capabilities

This scenario provides a complete, educational Docker networking experience that teaches real-world container communication patterns through hands-on experimentation, comprehensive debugging, and memorable "AHA!" moments.