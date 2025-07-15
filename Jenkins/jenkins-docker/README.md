# 🚀 Jenkins Docker Setup - CI/CD Chaos Workshop

## 🎯 Overview

This directory contains the Docker setup for running Jenkins locally to execute all CI/CD Chaos Workshop scenarios seamlessly. The Jenkins container is pre-configured with Docker-in-Docker support to run all workshop scenarios.

## 🏗️ Quick Start

### 1. Build the Jenkins Docker Image

```bash
# Navigate to the jenkins-docker directory
cd Jenkins/jenkins-docker

# Build the Jenkins image with Docker-in-Docker support
docker build -t jenkins-docker .
```

### 2. Run Jenkins Container

```bash
# Run Jenkins with Docker socket mounted for Docker-in-Docker
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

### 3. Access Jenkins

1. **Open your browser** and navigate to: `http://localhost:8080`
2. **Get the initial admin password**:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. **Follow the setup wizard** to complete Jenkins configuration

## 🔧 Advanced Configuration

### Environment Variables

You can customize the Jenkins setup with these environment variables:

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  -v jenkins_workspace:/workspace \
  -e JENKINS_OPTS="--httpPort=8080" \
  -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false" \
  --restart unless-stopped \
  jenkins-docker
```

### Volume Mounts Explained

- `/var/run/docker.sock`: Enables Docker-in-Docker for running containers
- `jenkins_home`: Persistent Jenkins data and configuration
- `jenkins_workspace`: Shared workspace for all scenarios

### Port Configuration

- `8080`: Jenkins web interface
- `50000`: Jenkins agent communication (for distributed builds)

## 🎯 Workshop Scenarios Setup

### 1. Install Required Jenkins Plugins

After Jenkins is running, install these plugins via **Manage Jenkins → Manage Plugins**:

**Core Plugins:**
- Pipeline: Declarative
- Docker Pipeline
- Credentials Plugin
- Credentials Binding Plugin
- Git plugin
- Git Parameter plugin

**Optional but Recommended:**
- Blue Ocean (for better pipeline visualization)
- HTML Publisher (for report viewing)
- Timestamper
- Build Timeout

### 2. Configure Docker Access

Ensure Jenkins can access Docker:

```bash
# Add jenkins user to docker group (if running on host)
sudo usermod -aG docker jenkins

# Or verify Docker access from within container
docker exec jenkins docker ps
```

### 3. Create Pipeline Jobs

Create Jenkins Pipeline jobs for each scenario:

#### Scenario 1: Docker Build Chaos
- **Job Name**: `scenario-01-docker-build`
- **Pipeline Script**: Copy from `Jenkins/jenkins_scenarios/scenario_01_docker_build/Jenkinsfile`

#### Scenario 2: Testcontainers Chaos
- **Job Name**: `scenario-02-testcontainers`
- **Pipeline Script**: Copy from `Jenkins/jenkins_scenarios/scenario_02_testcontainers/Jenkinsfile`

#### Scenario 3: HTML Reports Chaos
- **Job Name**: `scenario-03-html-reports`
- **Pipeline Script**: Copy from `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile`

#### Scenario 4: Secret Management Chaos
- **Job Name**: `scenario-04-secret-management`
- **Pipeline Script**: Copy from `Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Jenkinsfile`

#### Scenario 5: EKS Deployment Chaos
- **Job Name**: `scenario-05-eks-deployment`
- **Pipeline Script**: Copy from `Jenkins/jenkins_scenarios/scenario_05_deploy_eks/Jenkinsfile`

### 4. Configure AWS Credentials (for Scenario 5)

For EKS deployment scenarios, add AWS credentials:

1. Go to **Manage Jenkins → Credentials → System → Global credentials**
2. Click **Add Credentials**
3. Configure:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: Your AWS Access Key ID
   - **Password**: Your AWS Secret Access Key
   - **ID**: `aws-credentials`
   - **Description**: AWS credentials for EKS access

## 🚀 Running All Scenarios

### Method 1: Individual Pipeline Jobs

1. **Navigate to each job** in Jenkins UI
2. **Click "Build with Parameters"**
3. **Configure scenario-specific parameters**
4. **Click "Build"**

### Method 2: Automated Script

Use the provided script to run all scenarios:

```bash
# From the workshop root directory
python Jenkins/jenkins_scenarios/run_all_scenarios.py
```

### Method 3: Multi-Branch Pipeline

Create a multi-branch pipeline that automatically discovers and runs all scenarios:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Run All Scenarios') {
            parallel {
                stage('Scenario 1') {
                    steps {
                        build job: 'scenario-01-docker-build', parameters: [
                            string(name: 'APP_VERSION', value: '2')
                        ]
                    }
                }
                stage('Scenario 2') {
                    steps {
                        build job: 'scenario-02-testcontainers', parameters: [
                            choice(name: 'TEST_MODE', choices: ['pass'])
                        ]
                    }
                }
                // Add other scenarios...
            }
        }
    }
}
```

## 🔍 Monitoring and Debugging

### View Jenkins Logs

```bash
# View Jenkins container logs
docker logs jenkins

# Follow logs in real-time
docker logs -f jenkins
```

### Access Jenkins Container

```bash
# Execute commands inside Jenkins container
docker exec -it jenkins bash

# Check Docker access
docker exec jenkins docker ps

# Verify workspace
docker exec jenkins ls -la /workspace
```

### Troubleshooting Common Issues

#### 1. Docker Permission Issues
```bash
# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Or add jenkins user to docker group
sudo usermod -aG docker jenkins
```

#### 2. Port Already in Use
```bash
# Check what's using port 8080
sudo lsof -i :8080

# Stop existing Jenkins container
docker stop jenkins
docker rm jenkins
```

#### 3. Volume Mount Issues
```bash
# Create named volumes if they don't exist
docker volume create jenkins_home
docker volume create jenkins_workspace

# Check volume contents
docker run --rm -v jenkins_home:/data alpine ls -la /data
```

## 🧹 Cleanup

### Stop and Remove Jenkins Container

```bash
# Stop the container
docker stop jenkins

# Remove the container
docker rm jenkins

# Remove the image (optional)
docker rmi jenkins-docker
```

### Clean Up Volumes (⚠️ Destructive)

```bash
# Remove all Jenkins data
docker volume rm jenkins_home jenkins_workspace

# Or remove all unused volumes
docker volume prune
```

## 📊 Workshop Features

### ✅ What's Included

- **Docker-in-Docker Support**: Jenkins can build and run Docker containers
- **Persistent Storage**: Jenkins configuration and data persist across restarts
- **Scenario Isolation**: Each scenario runs in its own container environment
- **Real-time Monitoring**: Live pipeline execution and logging
- **Artifact Management**: Test reports and build artifacts are archived
- **Chaos Engineering**: Intentional failure scenarios for learning

### 🎯 Learning Outcomes

After running all scenarios, participants will understand:

- **Docker Build Pipelines**: Parameterized builds and container testing
- **Integration Testing**: Testcontainers with databases and services
- **Report Generation**: Enterprise-grade HTML reports and visualization
- **Security Scanning**: Secret detection and compliance reporting
- **Kubernetes Deployment**: EKS integration and kubectl troubleshooting
- **Chaos Engineering**: Intentional failure testing and recovery

## 🎉 Success Criteria

You've successfully set up the Jenkins environment when:

✅ **Jenkins is accessible** at http://localhost:8080  
✅ **Docker commands work** from within Jenkins  
✅ **All scenarios can be created** as Pipeline jobs  
✅ **Builds execute successfully** with proper parameters  
✅ **Reports are generated** and archived as artifacts  
✅ **Chaos scenarios fail predictably** and are handled gracefully  

---

## 🚀 Ready for Chaos!

Your Jenkins environment is now ready to run all CI/CD Chaos Workshop scenarios. Each scenario will teach different aspects of resilient pipeline design through controlled chaos and intentional failures.

**Remember**: Chaos is inevitable. Victory is optional. Choose wisely! 🎭 