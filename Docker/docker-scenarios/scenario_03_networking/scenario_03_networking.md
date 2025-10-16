# 🌐 Docker Networking Magic

**Experience real-world Docker networking problems and solutions**

Learn container communication, network isolation, and debugging techniques.

## 🚀 Quick Start

```bash
cd Docker/docker-scenarios/scenario_03_networking

# Run automated demo
python3 demo.py

# Clean up when done
python3 cleanup.py
```

## 📋 What You'll Learn

1. **App Without Database** - Shows container isolation
2. **Network Creation** - Custom Docker networks
3. **Container Communication** - Internal vs external access
4. **Network Inspection** - Debugging and monitoring

## 🎯 Demo Steps

### Step 1: App Without Database
- Build and run app container
- Show database connection failure
- Demonstrate container isolation

### Step 2: Adding Database with Network
- Create custom Docker network
- Start database container
- Connect app to database network
- Show successful communication

### Step 3: Network Inspection
- List Docker networks
- Inspect network configuration
- View container IP addresses

### Step 4: Internal Communication
- Test container-to-container communication
- Show external vs internal access
- Demonstrate network security

## 🔧 Prerequisites

- Docker installed and running
- ~500MB RAM available
- Port 8000 available
- `curl` and `jq` installed

## 🧪 Testing

```bash
# Test app endpoint
curl http://localhost:8000

# Test database connection
curl http://localhost:8000/db

# Inspect network
docker network ls
docker network inspect demo-network
```

## 🎯 Key Concepts

- **Container isolation** and networking
- **Custom Docker networks** for communication
- **Internal vs external** container access
- **Network inspection** and debugging
- **Service discovery** within networks

## 📊 Expected Results

- App fails without database (isolation)
- App succeeds with database (communication)
- Network inspection shows container connectivity
- Internal communication works, external is controlled

**Perfect for:** Understanding Docker networking, container communication, network debugging