# 🚀 Scenario 05: EKS Deployment Chaos - Complete Guide

## 🎯 **Scenario Overview**

This scenario demonstrates **real-world Kubernetes deployment patterns** using AWS EKS (Elastic Kubernetes Service). You'll learn how to:

- **Deploy applications to EKS clusters** using Jenkins pipelines
- **Handle deployment failures** and implement chaos engineering
- **Monitor deployments** with kubectl commands
- **Troubleshoot issues** in a production-like environment
- **Manage AWS credentials** securely in CI/CD pipelines

## 🛠️ **Technical Stack**

- **AWS EKS** - Managed Kubernetes service
- **Docker** - Containerized deployment tools
- **kubectl** - Kubernetes command-line tool
- **AWS CLI** - AWS service management
- **Jenkins** - CI/CD pipeline orchestration

## 📂 **Project Structure**

```
scenario_05_deploy_eks/
├── Dockerfile                    # ✅ Multi-stage build with AWS CLI and kubectl
├── Jenkinsfile                   # 🆕 NEW - Enhanced standardized pipeline
├── tests/                        # ✅ Test files for different scenarios
│   ├── test_kubectl_commands.py
│   ├── test_deployment.py
│   ├── test_service.py
│   └── generate_eks_report.py
├── manifests/                    # ✅ Kubernetes deployment manifests
│   ├── deployment-pass.yaml
│   ├── deployment-fail.yaml
│   ├── service.yaml
│   └── namespace.yaml
└── README.md                     # 🆕 This comprehensive guide
```

## 🚀 **Pipeline Features**

### **Enhanced Pipeline Structure**

The updated Jenkinsfile includes:
- ✅ **Standardized Environment Variables** - Uses consistent `SCENARIO_PATH`, `IMAGE_NAME`, `BUILD_TAG`
- ✅ **Robust Workspace Verification** - Checks for required files and shows workspace contents
- ✅ **Enhanced Error Handling** - Proper success/failure post actions with clear messaging
- ✅ **Consistent Stage Naming** - All stages use emojis and follow the same pattern as other scenarios

### **Pipeline Stages**

1. **Verify Local Workspace:** Shows workspace contents and checks for required files (Dockerfile)
2. **🔧 Build Docker Image:** Builds the deployment environment with AWS CLI and kubectl
3. **🧹 Pre-Cleanup:** Removes any leftover containers
4. **🚀 Run EKS Tests:** Executes deployment tests in parallel:
   - **🔧 kubectl Commands:** Tests basic kubectl functionality
   - **🚀 Deployment Tests:** Tests application deployment
   - **🌐 Service Tests:** Tests service creation and networking
5. **📋 Generate EKS Report:** Creates detailed deployment reports
6. **📦 Archive Reports:** Makes reports available as Jenkins artifacts

## ⚙️ **Running the Pipeline**

### **Parameters**

- `RUN_KUBECTL_TESTS` - Enable/disable kubectl command tests
- `RUN_DEPLOYMENT_TESTS` - Enable/disable deployment tests
- `RUN_SERVICE_TESTS` - Enable/disable service tests
- `KUBECTL_PASS` - Set kubectl tests to pass/fail mode
- `DEPLOYMENT_PASS` - Set deployment tests to pass/fail mode
- `VULNERABILITY_PASS` - Set service tests to pass/fail mode

### **Prerequisites**

1. **AWS EKS Cluster** - Must have an existing EKS cluster
2. **AWS Credentials** - Configured in Jenkins credential store
3. **Cluster Access** - Your AWS user must have kubectl access to the cluster
4. **Docker** - Available on Jenkins agent

## 🎯 **Test Scenarios**

### **✅ Pass Scenario**

The pass scenario demonstrates successful deployment:

1. **Authentication** - Validates AWS credentials and cluster access
2. **Namespace Creation** - Creates a dedicated namespace for testing
3. **Deployment** - Deploys a sample application with proper resources
4. **Service Creation** - Exposes the application via Kubernetes service
5. **Health Checks** - Verifies the deployment is healthy and accessible

### **❌ Fail Scenario**

The fail scenario demonstrates chaos engineering:

1. **Invalid Resources** - Deploys with impossibly low resource limits
2. **Broken Health Checks** - Uses incorrect health check endpoints
3. **Network Issues** - Creates service with wrong port configurations
4. **Rollback Testing** - Demonstrates proper failure handling and rollback

## 🔧 **Technical Implementation**

### **Docker Image Features**

The multi-stage Dockerfile includes:

- **AWS CLI** - For EKS cluster authentication
- **kubectl** - For Kubernetes operations
- **Python** - For test execution and reporting
- **Security** - Runs as non-root user
- **Optimization** - Layer caching for fast builds

### **Kubernetes Manifests**

The scenario includes realistic deployment manifests:

- **Namespace isolation** - Dedicated namespace for testing
- **Resource management** - Proper CPU/memory limits
- **Health checks** - Liveness and readiness probes
- **Service networking** - ClusterIP and LoadBalancer services
- **Security policies** - Pod security standards

## 📊 **Monitoring and Reporting**

### **Real-time Monitoring**

During deployment, you can monitor:

- **Pod Status** - `kubectl get pods -w`
- **Deployment Progress** - `kubectl rollout status`
- **Service Endpoints** - `kubectl get endpoints`
- **Events** - `kubectl get events --sort-by=.metadata.creationTimestamp`

### **Generated Reports**

The pipeline generates comprehensive reports including:

- **Deployment Status** - Success/failure indicators
- **Resource Usage** - CPU/memory consumption
- **Network Configuration** - Service and endpoint details
- **Error Analysis** - Detailed failure information
- **Performance Metrics** - Deployment timing and efficiency

## 🎓 **Learning Outcomes**

After completing this scenario, attendees understand:

- **Containerized CI/CD** - How to use Docker containers for consistent deployments
- **EKS Integration** - Real-world Kubernetes deployment patterns
- **Chaos Engineering** - Intentional failure testing and recovery
- **kubectl Mastery** - Essential commands for Kubernetes troubleshooting
- **Security** - AWS credential management in CI/CD pipelines
- **Monitoring** - Live deployment monitoring and event analysis

## ✅ **Success Criteria**

You've successfully completed Scenario 5 when:

✅ **Authentication Works**: Jenkins can authenticate to AWS and access EKS cluster  
✅ **Container Builds**: Docker image builds successfully with AWS CLI and kubectl  
✅ **Pass Scenario**: Successful deployment completes without errors  
✅ **Fail Scenario**: Chaos deployment demonstrates proper failure handling  
✅ **Live Monitoring**: Real-time kubectl commands show cluster status  
✅ **Troubleshooting**: You can interpret kubectl output and debug issues  
✅ **Cleanup**: Resources are properly cleaned up after tests  

## 🎉 **Advanced Extensions**

Ready for more challenges? Try these extensions:

### 🔄 Blue/Green Deployments
```bash
# Modify manifests to support blue/green deployments
# Add service selector switching
# Implement zero-downtime deployments
```

### 📊 Monitoring Integration
```bash
# Add Prometheus metrics collection
# Create Grafana dashboards
# Set up AlertManager rules
```

### 🔐 Security Enhancements
```bash
# Implement RBAC policies
# Add Pod Security Standards
# Configure Network Policies
```

### 🌐 Multi-Cluster Deployments
```bash
# Extend to deploy across multiple clusters
# Add region failover scenarios
# Implement cross-cluster networking
```

## 📚 **Additional Resources**

### Documentation Links
- [AWS EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/dockerfile_best-practices/)

### Sample Commands Reference

```bash
# EKS Cluster Management
aws eks list-clusters --region us-east-1
aws eks describe-cluster --name cluster-name --region us-east-1
aws eks update-kubeconfig --region us-east-1 --name cluster-name

# Kubernetes Deployment Commands
kubectl apply -f deployment.yaml
kubectl get deployments -o wide
kubectl describe deployment app-name
kubectl rollout status deployment/app-name
kubectl rollout history deployment/app-name

# Pod Management
kubectl get pods -l app=app-name -o wide
kubectl describe pod pod-name
kubectl logs pod-name --follow
kubectl exec -it pod-name -- /bin/bash

# Service and Networking
kubectl get services -o wide
kubectl describe service service-name
kubectl get endpoints
kubectl port-forward service/app-service 8080:80

# Troubleshooting Commands
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get events --field-selector type=Warning
kubectl top nodes
kubectl top pods

# Container and Image Management
docker build -t app:tag .
docker run --rm -it app:tag /bin/bash
docker logs container-id
docker exec -it container-id /bin/bash
```

## 🎯 **Workshop Facilitation Tips**

### For Instructors

**Timing Recommendations:**
- **Setup & Authentication**: 10-15 minutes
- **Pass Scenario Walkthrough**: 15-20 minutes  
- **Fail Scenario Deep Dive**: 20-25 minutes
- **Troubleshooting Practice**: 15-20 minutes
- **Q&A and Wrap-up**: 10-15 minutes

**Key Teaching Moments:**
1. **Authentication Flow**: Explain AWS IAM → EKS → kubectl chain
2. **Container Benefits**: Show how containerized tools ensure consistency
3. **Failure Analysis**: Walk through kubectl commands during fail scenario
4. **Real-world Parallels**: Connect chaos testing to production scenarios

### For Attendees

**Focus Areas:**
- Understand the kubectl command patterns
- Learn to read Kubernetes events and pod descriptions
- Practice troubleshooting failed deployments
- Recognize common deployment failure modes

**Hands-on Practice:**
- Run the authentication pipeline first
- Watch the console output carefully during both scenarios
- Try modifying the deployment manifests
- Experiment with kubectl commands

## 🔧 **Customization Options**

### Environment Variables

You can customize the scenario by modifying these environment variables in the Jenkinsfile:

```groovy
environment {
    SCENARIO_PATH = '/workspace/ci-cd-chaos-workshop/Jenkins/jenkins_scenarios/scenario_05_deploy_eks'
    IMAGE_NAME = "chaos-workshop-eks-deployment"
    BUILD_TAG = "${BUILD_NUMBER}"
    REPORTS_DIR = 'reports'
}
```

### Parameter Modifications

Adjust default values in the parameters section:

```groovy
parameters {
    booleanParam(
        name: 'RUN_KUBECTL_TESTS',
        defaultValue: true,
        description: '🔧 Run kubectl Command Tests'
    )
    booleanParam(
        name: 'RUN_DEPLOYMENT_TESTS',
        defaultValue: true,
        description: '🚀 Run Deployment Tests'
    )
}
```

### Custom Deployment Manifests

Create additional failure scenarios by modifying `deployment-fail.yaml`:

```yaml
# Example: Memory limit chaos
resources:
  limits:
    memory: "1Mi"  # Impossibly low limit
  requests:
    memory: "100Mi"

# Example: Invalid probe chaos
livenessProbe:
  httpGet:
    path: /nonexistent-endpoint
    port: 9999  # Wrong port
```

## 🚨 **Important Notes**

### Security Considerations

⚠️ **Credential Management**
- Never hardcode AWS credentials in Jenkinsfiles
- Use Jenkins credential store for secure credential handling
- Rotate credentials regularly

⚠️ **Container Security**
- The Dockerfile uses non-root user for running applications
- AWS CLI and kubectl run with appropriate permissions
- Consider using IAM roles for production deployments

⚠️ **Cluster Access**
- Test pipelines should use dedicated test clusters
- Implement proper RBAC for production environments
- Monitor and audit kubectl access

### Production Considerations

🏭 **Scaling for Production**
- Use dedicated Jenkins agents for Kubernetes deployments
- Implement proper resource quotas and limits
- Add monitoring and alerting for deployment failures
- Consider using GitOps tools like ArgoCD or Flux

🏭 **Multi-Environment Support**
- Extend parameters to support dev/staging/prod environments
- Implement environment-specific configuration management
- Add approval gates for production deployments

## 🐛 **Known Issues and Workarounds**

### Issue 1: aws-auth ConfigMap Access

**Problem:** New AWS users may not have kubectl access initially

**Workaround:** The JenkinsAuth pipeline will show your ARN - add it to the cluster's aws-auth ConfigMap

### Issue 2: Docker Layer Caching

**Problem:** Docker builds may be slow on first run

**Workaround:** The multi-stage Dockerfile is optimized for layer caching on subsequent builds

### Issue 3: EKS Cluster Warmup

**Problem:** Cold EKS clusters may take longer for first deployment

**Workaround:** The pipeline includes proper wait conditions and retry logic