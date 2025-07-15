#!/bin/bash

# Docker Image Scanner - Cleanup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}🔹 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${GREEN}🧹 Cleanup Script${NC}"
    echo "=================="
    echo ""
}

# Function to stop the application
stop_application() {
    print_step "Stopping Docker Image Scanner application..."
    
    # Kill the Python app process
    if pkill -f "python3 app.py" 2>/dev/null; then
        print_success "Application stopped"
    else
        print_warning "No application process found"
    fi
    
    # Also try python app.py
    if pkill -f "python app.py" 2>/dev/null; then
        print_success "Application stopped (python)"
    fi
}

# Function to clean up Docker images
cleanup_docker() {
    print_step "Cleaning up Docker images..."
    
    # Remove test images created during demo
    local test_images=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep -E "(test-|analyzer-)" 2>/dev/null || true)
    
    if [ -n "$test_images" ]; then
        echo "$test_images" | while read -r image; do
            print_step "Removing image: $image"
            docker rmi "$image" 2>/dev/null || print_warning "Could not remove $image"
        done
        print_success "Docker images cleaned up"
    else
        print_warning "No test images found"
    fi
}

# Function to clean up uploads directory
cleanup_uploads() {
    print_step "Cleaning up uploads directory..."
    
    if [ -d "uploads" ]; then
        local upload_count=$(find uploads -name "*.Dockerfile" 2>/dev/null | wc -l)
        if [ "$upload_count" -gt 0 ]; then
            rm -f uploads/*.Dockerfile
            print_success "Removed $upload_count uploaded files"
        else
            print_warning "No uploaded files found"
        fi
    else
        print_warning "Uploads directory not found"
    fi
}

# Function to clean up log files
cleanup_logs() {
    print_step "Cleaning up log files..."
    
    if [ -f "app.log" ]; then
        rm -f app.log
        print_success "Removed app.log"
    else
        print_warning "No app.log found"
    fi
}

# Main cleanup function
main() {
    print_header
    
    print_step "Starting cleanup process..."
    echo ""
    
    # Stop application
    stop_application
    
    # Clean up Docker
    cleanup_docker
    
    # Clean up uploads
    cleanup_uploads
    
    # Clean up logs
    cleanup_logs
    
    echo ""
    print_success "🎉 Cleanup completed successfully!"
    echo ""
    print_step "All resources have been cleaned up"
    print_step "You can now run the demo again with: ./demo_manual.sh or ./demo_simple.sh"
}

# Run cleanup
main 