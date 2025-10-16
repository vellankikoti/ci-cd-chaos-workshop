# 🛡️ Docker Resilience & Recovery Demo

**Transform fragile containers into bulletproof, self-healing systems!**

Experience real-world Docker resilience problems and solutions through hands-on interactive applications.

## 🎯 Overview

This scenario demonstrates Docker resilience through hands-on experience, showing how to transform fragile containers into bulletproof, self-healing systems with **100% uptime improvement** while implementing proper recovery mechanisms.

## 📁 Project Structure

```
scenario_02_resilience/
├── scenario_02_resilience.md      # This comprehensive guide
├── demo.py                        # Main demo script (run this!)
├── cleanup.py                     # Cleanup script
├── fragile_app.py                 # Fragile container demonstration app
├── resilient_app.py                # Resilience best practices demonstration app
├── app/
│   ├── app.py                     # Resilience dashboard app
│   ├── requirements.txt           # Dashboard dependencies
│   └── Dockerfile                 # Dashboard container
└── dockerfiles/
    ├── fragile.Dockerfile         # Fragile example (no resilience)
    └── resilient.Dockerfile       # Resilience-hardened (production-ready)
```

## 🚀 Quick Start

### Run the Demo
```bash
python3 demo.py
```

### Cleanup
```bash
python3 cleanup.py
```

## 🎓 What You'll Learn

### Core Resilience Concepts
- ❌ **Anti-patterns**: What makes Docker containers fragile
- ✅ **Health checks**: Container monitoring and recovery
- 🔄 **Auto-restart**: Self-healing container mechanisms
- 🛡️ **Resource limits**: Preventing container crashes
- 📊 **Monitoring**: Real-time resilience metrics

### Technical Skills
- Docker health check implementation
- Container restart policies
- Resource limit configuration
- Monitoring and alerting
- Production-ready resilience practices

## 🌐 Web Applications

### The demo launches 2 web applications:

| URL | Application | Purpose | Features |
|-----|-------------|---------|----------|
| `http://localhost:8000` | **Resilience Dashboard** | Real-time resilience analysis | • Live uptime monitoring<br>• Recovery metrics tracking<br>• Health check status<br>• Auto-refresh metrics |
| `http://localhost:8001` | **Fragile App** | Fragility anti-pattern demo | • No health checks<br>• No restart policies<br>• Resource exhaustion<br>• Failure visualization |
| `http://localhost:8002` | **Resilient App** | Resilience best practices | • Health check integration<br>• Auto-restart policies<br>• Resource limits<br>• Self-healing benefits |

## 📊 Results You'll See

### Resilience Comparison
```
Fragile Container:     🔴 0% Uptime (❌ Constant failures)
Resilient Container:   🟢 100% Uptime (✅ Self-healing)
Improvement:           🎯 100% resilience enhancement
```

### Recovery Analysis
```
Fragile Issues:        10+ failure points
Resilient Issues:      0 failure points
Recovery Time:         100% improvement
Auto-healing:          Enabled
```

### Resilience Features
- ✅ **Health checks** vs no monitoring
- ✅ **Auto-restart** vs manual intervention
- ✅ **Resource limits** vs unlimited consumption
- ✅ **Graceful shutdown** vs abrupt failures

## 🎪 Workshop Features

### Educational Progression
1. **Problem Demonstration** - See fragile container failing
2. **Solution Implementation** - Watch resilience hardening in action
3. **Visual Comparison** - Interactive dashboard analysis
4. **Hands-on Exploration** - Try all three applications
5. **Technical Deep-dive** - Resilience monitoring and metrics

### Presenter-Friendly
- 📖 **Educational context** provided at each step
- ⏸️ **Automatic pauses** for audience absorption
- 🎨 **Visual interfaces** keep attention
- 🔄 **Graceful interruption** with Ctrl+C
- 🧹 **Automatic cleanup** when complete

## 🔧 Technical Requirements

### Prerequisites
- Docker Desktop installed and running
- Python 3.6+
- 1GB+ available disk space (temporary)
- Ports 8000, 8001, 8002 available (for interactive demo)

### Dependencies
All Python packages are automatically installed:
- `flask` - Web framework
- `docker` - Docker API integration
- `psutil` - System monitoring
- `requests` - HTTP client

## 🎯 Use Cases

### Perfect For:
- **Docker resilience workshops** and training sessions
- **Conference presentations** with live resilience demos
- **Team training** on resilience best practices
- **DevOps education** and reliability awareness
- **Self-learning** Docker resilience concepts

### Audience:
- **All Levels**: Run `python3 demo.py` - it's comprehensive yet beginner-friendly
- **Advanced**: Explore the Dockerfiles and implementation details
- **Trainers**: Use the demo for engaging, hands-on presentations

## 🚨 Troubleshooting

### Common Issues

**Ports already in use:**
```bash
# Check what's using the ports
lsof -i :8000 -i :8001 -i :8002

# Kill processes if needed
sudo pkill -f "python.*app.py"
```

**Docker build fails:**
```bash
# Clean up Docker
docker system prune -f
docker volume prune -f
```

**Demo interrupted:**
```bash
# Manual cleanup
python3 cleanup.py
```

**Applications not accessible:**
- Wait 5-10 seconds after "starting" messages
- Check Docker containers are running: `docker ps`
- Verify ports aren't blocked by firewall

## 📚 Additional Resources

### Learn More
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Container Restart Policies](https://docs.docker.com/config/containers/start-containers-automatically/)
- [Resource Limits](https://docs.docker.com/config/containers/resource_constraints/)

### Files Explained
- `fragile.Dockerfile` - Demonstrates common Docker resilience anti-patterns
- `resilient.Dockerfile` - Shows resilience-hardened best practices  
- `fragile_app.py` - Visual "what NOT to do" web application
- `resilient_app.py` - Visual resilience best practices web application
- `app/app.py` - Live resilience dashboard with Docker integration

## 🤝 Contributing

This demo is designed to be:
- **Educational** - Easy to understand and learn from
- **Practical** - Real-world applicable resilience techniques
- **Engaging** - Interactive and visually appealing
- **Professional** - Workshop and presentation ready

Feel free to customize the applications or add additional resilience features to enhance the learning experience!

## 🎉 Success Metrics

After completing this demo, you should understand:
- ✅ Why Docker resilience matters in production
- ✅ How to implement proper health checks
- ✅ How to configure auto-restart policies
- ✅ Resource limit implications
- ✅ Best practices for container resilience

**Ready to make your containers bulletproof? Choose your demo and let's build resilience! 🛡️**
