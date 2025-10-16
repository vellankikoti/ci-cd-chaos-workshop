# 🚀 Jenkins CI/CD Scenarios - Complete Learning Path

**Master Jenkins from basics to advanced through hands-on, interactive scenarios!**

## 📚 Overview

This collection contains 3 progressive Jenkins scenarios designed to take you from beginner to expert in CI/CD pipelines. Each scenario builds upon the previous one, introducing new concepts and best practices.

**📖 Additional Resources:**
- [Complete Scenario Comparison](./SCENARIO_COMPARISON.md) - Visual comparison and learning guide
- [Scenario 3 Enhancements](./scenario_03_jenkins_powerhouse/ENHANCEMENTS.md) - What makes Scenario 3 special

---

## 🎯 Scenario Comparison Matrix

| Feature | Scenario 1 | Scenario 2 | Scenario 3 |
|---------|-----------|-----------|-----------|
| **Difficulty** | 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced |
| **Duration** | 5 mins | 10 mins | 15 mins |
| **Parameters** | None | 5 params | 8 params |
| **Environments** | Single | Multi (3) | Multi (3) + Strategies |
| **Testing** | Basic | Conditional | Comprehensive (4 types) |
| **Deployment** | Simple | Smart | Blue-Green/Rolling/Canary |
| **Monitoring** | None | Basic | Real-time + APIs |
| **Security** | None | Optional | Integrated |
| **Docker** | Static | Dynamic | Multi-stage |
| **Parallelization** | No | No | Yes (Tests) |
| **Web Dashboard** | Static | Dynamic | Interactive + Live Updates |

---

## 📖 Detailed Scenario Breakdown

### 🟢 [Scenario 1: Jenkins Pipeline Fundamentals](./scenario_01_simple_pipeline/)

**What You'll Learn:**
- ✅ Basic Jenkins pipeline structure
- ✅ Simple stage definitions
- ✅ Sequential execution
- ✅ Basic Docker integration
- ✅ Static web application deployment
- ✅ Console output formatting

**Key Concepts:**
- Declarative pipeline syntax
- Stage organization
- Basic shell commands
- Docker build and run
- Simple HTML generation

**What's Installed/Used:**
- Jenkins (declarative pipeline)
- Docker (for containerization)
- Python 3 (for HTML generation)
- Basic HTTP server

**Best For:**
- First-time Jenkins users
- Understanding CI/CD fundamentals
- Learning pipeline basics
- Quick wins and confidence building

---

### 🟡 [Scenario 2: Parameterized Builds](./scenario_02_parameterized_builds/)

**What You'll Learn:**
- ✅ Parameterized builds (5 parameters)
- ✅ Conditional logic and decision making
- ✅ Multi-environment configurations (Dev/Staging/Prod)
- ✅ Dynamic Docker image creation
- ✅ Environment-specific configurations
- ✅ Feature-based deployments (Basic/Advanced/Enterprise)
- ✅ Smart port management
- ✅ Deployment strategies

**Key Concepts:**
- Jenkins parameters (choice, string, boolean)
- Environment-specific logic
- Dynamic Dockerfile generation
- Package manager compatibility (apt-get vs apk)
- Resource allocation per environment
- Port conflict resolution

**What's Installed/Used:**
- Jenkins with parameterized builds
- Docker with environment-specific base images
  - Development: `python:3.11-slim` (Debian-based)
  - Staging: `python:3.11-alpine` (Alpine-based)
  - Production: `python:3.11-slim` (Debian-based)
- Dynamic package management:
  - **Basic**: Core packages only
  - **Advanced**: + curl, jq, redis, postgresql-client
  - **Enterprise**: + nginx, monitoring tools
- Python HTTP server with API endpoints

**Environment Configurations:**

**Development:**
- Purpose: Fast iteration and testing
- Database: Local SQLite
- Logging: Debug level
- Resources: 1 CPU, 512MB RAM
- Monitoring: Basic
- Security: Relaxed

**Staging:**
- Purpose: Pre-production validation
- Database: PostgreSQL
- Logging: Info level
- Resources: 2 CPU, 1GB RAM
- Monitoring: Full
- Security: Standard

**Production:**
- Purpose: Live user traffic
- Database: PostgreSQL Cluster
- Logging: Warning level
- Resources: 4 CPU, 4GB RAM
- Monitoring: Advanced + Alerts
- Security: Maximum

**Best For:**
- Understanding configuration management
- Learning environment-specific deployments
- Practicing conditional logic
- Real-world deployment scenarios

---

### 🔴 [Scenario 3: Jenkins Powerhouse](./scenario_03_jenkins_powerhouse/)

**What You'll Learn:**
- ✅ Advanced parameterization (8 parameters)
- ✅ Parallel test execution (4 test types simultaneously)
- ✅ Comprehensive testing suite (Unit/Integration/Security/Performance)
- ✅ Advanced deployment strategies (Blue-Green/Rolling/Canary)
- ✅ Real-time monitoring and metrics
- ✅ Interactive web dashboard with live updates
- ✅ Security scanning and compliance
- ✅ Multi-stage Docker builds
- ✅ Health checks and observability
- ✅ Retry mechanisms and error handling

**Key Concepts:**
- Jenkins retry and timeout options
- Parallel stage execution
- Conditional test execution (when blocks)
- Advanced Docker multi-stage builds
- API-driven applications
- Real-time metrics collection
- Deployment strategy implementation
- Container health checks
- Resource optimization

**What's Installed/Used:**
- Jenkins with advanced features:
  - `retry(2)` - Auto-retry failed builds
  - `timeout(30 minutes)` - Build timeout
  - `timestamps()` - Timestamped output
  - `buildDiscarder` - Keep last 10 builds
- Docker with advanced features:
  - Multi-stage builds
  - HEALTHCHECK directives
  - Dynamic port mapping
  - Environment-specific optimizations
- Python 3 with advanced HTTP server:
  - Multiple API endpoints (/api/status, /api/metrics, /api/health)
  - Real-time data generation
  - CORS support
  - JSON responses
- Testing frameworks (simulated):
  - Unit testing (127 tests)
  - Integration testing (API + DB)
  - Security testing (OWASP ZAP, SAST)
  - Performance testing (load tests)

**Advanced Features:**

**Parallel Test Execution:**
```
🧪 Comprehensive Testing Suite
├── Unit Tests (parallel)
├── Integration Tests (parallel)
├── Security Tests (parallel - conditional)
└── Performance Tests (parallel - conditional)
```

**Deployment Strategies:**
- **Blue-Green**: Zero-downtime with instant rollback
  - Deploy to green environment
  - Health check validation
  - Switch traffic
  - Keep blue for rollback

- **Rolling**: Gradual instance replacement
  - Deploy to subset of instances
  - Validate health
  - Gradually replace remaining
  - Monitor throughout

- **Canary**: Progressive traffic shifting
  - Deploy to small percentage
  - Monitor metrics
  - Gradually increase traffic
  - Full deployment after validation

**Interactive Dashboard:**
- **Live Metrics**: Real-time CPU, memory, disk usage
- **Business Metrics**: Users online, transactions, revenue
- **Health Status**: Database, cache, storage, network checks
- **API Endpoints**:
  - `/api/status` - Application status and configuration
  - `/api/metrics` - System and application metrics
  - `/api/health` - Health check results
- **Auto-refresh**: JavaScript-powered live updates
- **Environment-specific themes**:
  - Development: Green gradient
  - Staging: Yellow gradient
  - Production: Red gradient

**Security Features:**
- OWASP ZAP vulnerability scanning
- Dependency security checks
- SAST (Static Application Security Testing)
- Secrets scanning
- Security score calculation
- Compliance validation

**Best For:**
- Production-ready pipelines
- Enterprise deployments
- Complex multi-environment setups
- Security-conscious organizations
- Performance-critical applications
- Teams needing observability

---

## 🎓 Learning Path Recommendation

### **Beginner Path (Day 1)**
1. Start with **Scenario 1** (15 minutes)
   - Run the basic pipeline
   - Understand stages
   - See Docker in action
   - Access the web application

### **Intermediate Path (Day 2-3)**
2. Move to **Scenario 2** (30 minutes)
   - Experiment with all 5 parameters
   - Try each environment (Dev/Staging/Prod)
   - Test each feature set (Basic/Advanced/Enterprise)
   - Compare environment differences
   - Observe conditional deployments

### **Advanced Path (Day 4-7)**
3. Master **Scenario 3** (60 minutes)
   - Configure all 8 parameters
   - Run parallel tests
   - Try each deployment strategy
   - Monitor live metrics
   - Test API endpoints
   - Implement security scanning
   - Observe health checks

---

## 🔧 Prerequisites

### **System Requirements:**
- Jenkins server (2.0+)
- Docker (20.0+)
- Python 3 (3.8+)
- 4GB RAM minimum
- 10GB disk space

### **Knowledge Requirements:**
- **Scenario 1**: None (absolute beginner-friendly)
- **Scenario 2**: Basic Jenkins knowledge
- **Scenario 3**: Jenkins + Docker experience

---

## 🚀 Quick Start Guide

### **1. Clone Repository**
```bash
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop
cd ci-cd-chaos-workshop/Jenkins/jenkins-scenarios
```

### **2. Create Jenkins Job**
For each scenario:
1. Jenkins Dashboard → New Item
2. Enter name (e.g., `scenario_01_simple_pipeline`)
3. Select "Pipeline" → OK
4. Configure:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop`
   - Branch: `*/main`
   - Script Path: `Jenkins/jenkins-scenarios/[scenario_name]/Jenkinsfile`

### **3. Run Pipeline**
- **Scenario 1**: Click "Build Now"
- **Scenario 2-3**: Click "Build with Parameters" → Configure → Build

---

## 📊 Comparison: What Makes Each Scenario Unique?

### **Scenario 1: Foundation**
- Single static configuration
- Linear execution (A → B → C → D)
- Basic Docker usage
- Simple HTML output
- **Focus**: Understanding Jenkins basics

### **Scenario 2: Flexibility**
- 3,750 possible configurations (5 parameters with various values)
- Conditional execution based on parameters
- Dynamic Docker images per environment
- Interactive web application with parameter-based styling
- **Focus**: Configuration management and environment handling

### **Scenario 3: Power**
- 15,552 possible configurations (8 parameters)
- Parallel execution (4 tests running simultaneously)
- Multi-stage Docker builds with health checks
- Live interactive dashboard with real-time APIs
- 3 deployment strategies
- 4 test types
- **Focus**: Production-ready, enterprise-grade pipelines

---

## 🎯 Success Metrics

### **Scenario 1 Success:**
- ✅ Pipeline completes in < 2 minutes
- ✅ Docker container runs successfully
- ✅ Web page accessible on assigned port
- ✅ Understand basic Jenkins pipeline structure

### **Scenario 2 Success:**
- ✅ Can run with different parameter combinations
- ✅ Understand environment differences
- ✅ Docker image changes based on configuration
- ✅ Web application reflects parameter choices

### **Scenario 3 Success:**
- ✅ Parallel tests execute simultaneously
- ✅ API endpoints return real-time data
- ✅ Can switch between deployment strategies
- ✅ Dashboard updates in real-time
- ✅ Health checks pass
- ✅ Understand production pipeline patterns

---

## 🔍 Troubleshooting Common Issues

### **Port Conflicts**
- **Problem**: Port 8080 already in use
- **Solution**: Scenarios 2 & 3 automatically find available ports (8081, 8082, etc.)

### **Docker Permission Errors**
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### **Build Failures**
1. Check Jenkins console output
2. Verify Docker daemon is running: `docker ps`
3. Check available disk space: `df -h`
4. Review system resources: `free -h`

---

## 🤝 Contributing

Want to add more scenarios? Follow these guidelines:
1. Create new directory: `scenario_XX_name/`
2. Include: Jenkinsfile, README.md, and any additional files
3. Update this master README
4. Test thoroughly with different configurations

---

## 📚 Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Docker Documentation](https://docs.docker.com/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🎉 Congratulations!

By completing all 3 scenarios, you've mastered:
- ✅ Jenkins pipeline fundamentals
- ✅ Parameterized and conditional builds
- ✅ Multi-environment deployments
- ✅ Docker integration and optimization
- ✅ Testing strategies
- ✅ Deployment strategies
- ✅ Monitoring and observability
- ✅ Security best practices
- ✅ Production-ready CI/CD patterns

**You're now ready to build world-class CI/CD pipelines!** 🚀✨

---

*These scenarios are part of the CI/CD Chaos Workshop for PyConES 2025*
