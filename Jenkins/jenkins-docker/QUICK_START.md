# 🚀 Quick Start - Jenkins Docker Setup

## ⚡️ One-Command Setup

```bash
# Navigate to jenkins-docker directory
cd Jenkins/jenkins-docker

# Run the automated setup script
./setup.sh
```

## 🔧 Manual Setup (Alternative)

### 1. Build Image
```bash
cd Jenkins/jenkins-docker
docker build -t jenkins-docker .
```

### 2. Run Container
```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  -v jenkins_workspace:/workspace \
  --restart unless-stopped \
  jenkins-docker
```

### 3. Get Admin Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 4. Access Jenkins
Open: http://localhost:8080

## 🎯 Workshop Scenarios

After Jenkins is running, create these Pipeline jobs:

| Scenario | Job Name | Jenkinsfile Location |
|----------|----------|---------------------|
| Docker Build Chaos | `scenario-01-docker-build` | `Jenkins/jenkins_scenarios/scenario_01_docker_build/Jenkinsfile` |
| Testcontainers Chaos | `scenario-02-testcontainers` | `Jenkins/jenkins_scenarios/scenario_02_testcontainers/Jenkinsfile` |
| HTML Reports Chaos | `scenario-03-html-reports` | `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile` |
| Secret Management Chaos | `scenario-04-secret-management` | `Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Jenkinsfile` |
| EKS Deployment Chaos | `scenario-05-eks-deployment` | `Jenkins/jenkins_scenarios/scenario_05_deploy_eks/Jenkinsfile` |

## 🔍 Useful Commands

```bash
# View logs
docker logs jenkins

# Access container
docker exec -it jenkins bash

# Stop Jenkins
docker stop jenkins

# Remove Jenkins
docker rm jenkins

# Check Docker access from Jenkins
docker exec jenkins docker ps
```

## 🛠️ Troubleshooting

### Port 8080 Already in Use
```bash
# Find what's using the port
sudo lsof -i :8080

# Stop existing service or change port in setup script
```

### Docker Permission Issues
```bash
# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock
```

### Jenkins Not Starting
```bash
# Check container logs
docker logs jenkins

# Verify Docker socket mount
docker exec jenkins docker ps
```

## 🎉 Success Indicators

✅ Jenkins accessible at http://localhost:8080  
✅ Admin password retrieved successfully  
✅ Docker commands work from Jenkins container  
✅ All workshop scenarios can be created as Pipeline jobs  

---

**Ready for Chaos! 🎭** 