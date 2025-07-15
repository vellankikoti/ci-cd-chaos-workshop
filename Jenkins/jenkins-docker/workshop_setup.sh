#!/bin/bash

# 🚀 Jenkins CI/CD Chaos Workshop - One-Command Setup Script
# This script builds Jenkins, starts the container, syncs your workspace, and verifies everything.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Config
JENKINS_IMAGE="jenkins-docker"
JENKINS_CONTAINER="jenkins"
JENKINS_PORT="8080"
JENKINS_AGENT_PORT="50000"
WORKSPACE_MOUNT="jenkins_workspace:/workspace"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# 1. Docker Permissions
fix_docker_permissions() {
    print_info "Checking Docker availability..."
    
    # First check if Docker is already working
    if docker info > /dev/null 2>&1; then
        print_status "Docker is already working - no permission fixes needed"
        return 0
    fi
    
    print_info "Docker not accessible - checking permissions..."
    
    # Check if user is in docker group
    if groups | grep -q docker; then
        print_status "User is in docker group - no sudo needed"
        # Try to fix permissions without sudo first
        if chmod 666 /var/run/docker.sock 2>/dev/null; then
            print_status "Docker socket permissions updated (no sudo needed)"
        else
            print_warning "Could not update Docker socket permissions without sudo"
            print_info "Docker should still work if you're in the docker group"
        fi
    else
        print_warning "User not in docker group - trying with sudo"
        if [ -S /var/run/docker.sock ]; then
            sudo chmod 666 /var/run/docker.sock 2>/dev/null || {
                print_warning "Could not fix Docker socket permissions with sudo"
                print_info "You may need to run: sudo chmod 666 /var/run/docker.sock"
                print_info "Or add your user to docker group: sudo usermod -aG docker $USER"
            }
            print_status "Docker socket permissions updated with sudo"
        else
            print_warning "Docker socket not found at /var/run/docker.sock"
        fi
    fi
}

# 2. Build Jenkins Image
build_jenkins_image() {
    print_info "Building Jenkins Docker image..."
    docker build -t ${JENKINS_IMAGE} .
    print_status "Jenkins image built successfully"
}

# 3. Start Jenkins Container
start_jenkins_container() {
    print_info "Starting Jenkins container..."
    if docker ps -a --format "table {{.Names}}" | grep -q "^${JENKINS_CONTAINER}$"; then
        print_warning "Found existing Jenkins container, stopping and removing..."
        docker stop ${JENKINS_CONTAINER} 2>/dev/null || true
        docker rm ${JENKINS_CONTAINER} 2>/dev/null || true
        print_status "Existing container cleaned up"
    fi
    docker volume create jenkins_home 2>/dev/null || print_warning "jenkins_home volume already exists"
    docker volume create jenkins_workspace 2>/dev/null || print_warning "jenkins_workspace volume already exists"
    docker run -d \
        --name ${JENKINS_CONTAINER} \
        -p ${JENKINS_PORT}:8080 \
        -p ${JENKINS_AGENT_PORT}:50000 \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v jenkins_home:/var/jenkins_home \
        -v jenkins_workspace:/workspace \
        --restart unless-stopped \
        --user root \
        ${JENKINS_IMAGE}
    print_status "Jenkins container started as root"
}

# 4. Sync Workspace
sync_workspace() {
    print_info "Copying workshop files from $PROJECT_ROOT to Jenkins container..."
    docker cp "$PROJECT_ROOT" jenkins:/workspace/ci-cd-chaos-workshop
    print_status "Workshop files copied successfully to Jenkins container."
}

# 5. Wait for Jenkins
wait_for_jenkins() {
    print_info "Waiting for Jenkins to be ready..."
    local max_attempts=30
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:${JENKINS_PORT} > /dev/null 2>&1; then
            print_status "Jenkins is ready!"
            return 0
        fi
        print_info "Attempt $attempt/$max_attempts: Jenkins not ready yet, waiting..."
        sleep 5
        attempt=$((attempt + 1))
    done
    print_error "Jenkins failed to start within the expected time"
    print_info "Check container logs with: docker logs ${JENKINS_CONTAINER}"
    exit 1
}

# 6. Verification
verify_setup() {
    print_info "Verifying Docker access from Jenkins..."
    if docker exec jenkins docker ps > /dev/null 2>&1; then
        print_status "Docker access from Jenkins verified"
    else
        print_error "Docker access from Jenkins failed"
        exit 1
    fi
    print_info "Verifying workshop files in Jenkins workspace..."
    if docker exec jenkins test -f /workspace/ci-cd-chaos-workshop/Jenkins/jenkins_scenarios/scenario_01_docker_build/Dockerfile; then
        print_status "Workshop files are available in Jenkins workspace"
    else
        print_error "Workshop files are missing from Jenkins workspace"
        exit 1
    fi
    print_info "Verifying Jenkins web access..."
    if curl -s http://localhost:${JENKINS_PORT} > /dev/null 2>&1; then
        print_status "Jenkins web interface is accessible"
    else
        print_error "Jenkins web interface is not accessible"
        exit 1
    fi
}

# 7. Show Admin Password
show_admin_password() {
    print_info "Getting initial admin password..."
    sleep 5
    if docker exec ${JENKINS_CONTAINER} test -f /var/jenkins_home/secrets/initialAdminPassword; then
        local password=$(docker exec ${JENKINS_CONTAINER} cat /var/jenkins_home/secrets/initialAdminPassword)
        print_status "Initial admin password: ${password}"
        echo ""
        print_info "🔐 Save this password - you'll need it to complete Jenkins setup"
    else
        print_warning "Could not retrieve initial admin password"
        print_info "You may need to check the container logs or wait a bit longer"
    fi
}

# 8. Final Instructions
show_final_instructions() {
    echo ""
    echo -e "${GREEN}🎉 Jenkins Workshop Setup Complete!${NC}"
    echo "=================================="
    echo ""
    print_info "Access Jenkins at: http://localhost:${JENKINS_PORT}"
    echo ""
    print_info "Next steps:"
    echo "1. Open http://localhost:${JENKINS_PORT} in your browser"
    echo "2. Use the admin password shown above"
    echo "3. Install suggested plugins"
    echo "4. Create your admin user"
    echo "5. Sync your workspace with this script after any changes"
    echo "6. Create pipeline jobs and copy Jenkinsfile content from /workspace/ci-cd-chaos-workshop"
    echo ""
    print_info "Useful commands:"
    echo "• View logs: docker logs ${JENKINS_CONTAINER}"
    echo "• Access container: docker exec -it ${JENKINS_CONTAINER} bash"
    echo "• Stop Jenkins: docker stop ${JENKINS_CONTAINER}"
    echo "• Remove Jenkins: docker rm ${JENKINS_CONTAINER}"
    echo "• Test Docker: docker exec ${JENKINS_CONTAINER} docker ps"
    echo ""
    print_info "Workshop scenarios are ready to be configured in Jenkins!"
    echo ""
}

# Main
main() {
    echo -e "${BLUE}🚀 Jenkins CI/CD Chaos Workshop - One-Command Setup${NC}"
    echo "=================================================="
    fix_docker_permissions
    build_jenkins_image
    start_jenkins_container
    sync_workspace
    wait_for_jenkins
    verify_setup
    show_admin_password
    show_final_instructions
}

main "$@" 