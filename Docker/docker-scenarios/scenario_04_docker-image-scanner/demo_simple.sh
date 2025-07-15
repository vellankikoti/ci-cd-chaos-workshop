#!/bin/bash

# Docker Image Scanner - Simple Demo Script
# Quick demonstration of key features

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}🔹 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if application is running
check_app_running() {
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start the application
start_application() {
    print_header "Starting Docker Image Scanner"
    echo "================================"
    
    # Check if app is already running
    if check_app_running; then
        print_success "Application is already running on http://localhost:8000"
        return 0
    fi
    
    print_step "Starting application..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not available"
        exit 1
    fi
    
    # Start the application
    python3 app.py > app.log 2>&1 &
    APP_PID=$!
    
    # Wait for application to start
    print_step "Waiting for application to start..."
    local attempts=0
    while [ $attempts -lt 30 ]; do
        if check_app_running; then
            print_success "Application is running!"
            break
        fi
        echo -n "."
        sleep 2
        attempts=$((attempts + 1))
    done
    
    if [ $attempts -eq 30 ]; then
        print_error "Application failed to start"
        exit 1
    fi
    
    echo ""
    print_success "🎉 Ready! Open http://localhost:8000"
    echo ""
}

# Function to run quick demo
run_quick_demo() {
    print_header "Quick Demo - Key Features"
    echo "============================"
    echo ""
    echo "This demo will quickly show the main features:"
    echo ""
    echo "1. 🔍 Image Analysis"
    echo "   • Enter: nginx:1.25-alpine (secure)"
    echo "   • Enter: python:3.8 (vulnerable)"
    echo ""
    echo "2. 🐳 Dockerfile Analysis"
    echo "   • Upload: simple_dockerfiles/Dockerfile_secure_python.txt"
    echo "   • Upload: simple_dockerfiles/Dockerfile_vulnerable_python.txt"
    echo ""
    echo "3. ⚖️  Image Comparison"
    echo "   • Compare: python:3.8 vs python:3.11-slim"
    echo "   • Compare: nginx:1.25-alpine vs ubuntu:22.04"
    echo ""
    echo "4. 📊 Educational Insights"
    echo "   • Show vulnerability details"
    echo "   • Explain security scores"
    echo "   • Discuss best practices"
    echo ""
    print_step "Application is running at: http://localhost:8000"
    print_step "Follow the steps above to demonstrate the features"
    echo ""
    print_warning "Press Ctrl+C to stop the application when done"
    
    # Keep the script running
    while true; do
        sleep 1
    done
}

# Cleanup function
cleanup() {
    echo ""
    print_step "Cleaning up..."
    pkill -f "python3 app.py" 2>/dev/null || true
    print_success "Demo completed!"
}

# Set up trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    print_header "🐳 Docker Image Scanner - Quick Demo"
    echo "========================================="
    echo ""
    echo "This is a quick demonstration of Docker security scanning."
    echo "The application will start and you can show the key features."
    echo ""
    
    # Check Docker
    print_step "Checking Docker..."
    if ! docker ps > /dev/null 2>&1; then
        print_error "Docker is not running"
        exit 1
    fi
    print_success "Docker is running"
    
    # Start application
    start_application
    
    # Run quick demo
    run_quick_demo
}

# Run the demo
main 