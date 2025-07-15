#!/bin/bash

# 🚀 Docker Networking Magic - Automated Demo Script
# ==================================================
# This script runs the networking scenario automatically
# for quick testing and demonstrations.

set -e

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print headers
print_header() {
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}========================================${NC}\n"
}

# Function to print steps
print_step() {
    echo -e "${BLUE}➤ $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print warnings
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to print errors
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print info
print_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}"
}

# Function to test app endpoint
test_app_endpoint() {
    local url="http://localhost:5000"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
    done
    return 1
}

# Function to test voting functionality
test_voting() {
    # First, get initial vote count
    local initial_count=$(curl -s http://localhost:5000 | awk '/WFH Votes/{getline; print}' | grep -o '[0-9]\+' | head -1 || echo "0")
    
    # Submit a vote
    if curl -s -X POST -d "vote=wfh" http://localhost:5000 >/dev/null 2>&1; then
        # Wait a moment for the vote to be processed
        sleep 2
        
        # Get the new vote count
        local new_count=$(curl -s http://localhost:5000 | awk '/WFH Votes/{getline; print}' | grep -o '[0-9]\+' | head -1 || echo "0")
        
        # Ensure we have valid numbers
        if [[ "$initial_count" =~ ^[0-9]+$ ]] && [[ "$new_count" =~ ^[0-9]+$ ]]; then
            # Check if the vote count increased
            if [ "$new_count" -gt "$initial_count" ]; then
                return 0  # Vote was recorded successfully
            else
                return 1  # Vote was not recorded
            fi
        else
            return 1  # Invalid vote counts
        fi
    else
        return 1  # POST request failed
    fi
}

# Function to cleanup
cleanup() {
    print_step "Cleaning up containers and networks..."
    docker rm -f vote-app redis-server 2>/dev/null || true
    docker network rm vote-net 2>/dev/null || true
    print_success "Cleanup completed"
}

# Main demo function
run_demo() {
    print_header "🚀 Docker Networking Magic - Automated Demo"
    echo -e "${CYAN}Running the complete networking scenario automatically...${NC}"
    echo ""
    
    # Initial cleanup
    print_header "🧹 Initial Cleanup"
    cleanup
    sleep 2
    
    # Step 1: Run app without database
    print_header "🔴 STEP 1: App Without Database (Expected Failure)"
    print_step "Building the Flask voting app..."
    docker build -t vote-app ./app
    print_success "App built successfully"
    
    print_step "Running app without Redis database..."
    docker run -d --name vote-app -p 5000:5000 vote-app
    print_success "App container started"
    
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        print_info "Testing voting (should fail)..."
        if test_voting; then
            print_warning "Voting worked (unexpected in this scenario)"
        else
            print_success "Voting failed as expected - no database connection!"
        fi
    else
        print_error "App is not responding"
    fi
    
    sleep 3
    
    # Step 2: Add database in wrong network
    print_header "🔴 STEP 2: Database in Wrong Network (Expected Failure)"
    print_step "Cleaning up previous app..."
    docker rm -f vote-app 2>/dev/null || true
    
    print_step "Starting Redis database..."
    docker run -d --name redis-server redis:alpine
    print_success "Redis container started"
    
    print_step "Starting app with Redis hostname (wrong network)..."
    docker run -d --name vote-app -p 5000:5000 -e REDIS_HOST=redis-server vote-app
    print_success "App container started with Redis hostname"
    
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        print_info "Testing voting (should fail)..."
        if test_voting; then
            print_warning "Voting worked (unexpected in this scenario)"
        else
            print_success "Voting failed as expected - network isolation!"
        fi
    else
        print_error "App is not responding"
    fi
    
    sleep 3
    
    # Step 3: Fix the network
    print_header "🟢 STEP 3: Fix the Network (Success!)"
    print_step "Cleaning up previous containers..."
    docker rm -f vote-app redis-server 2>/dev/null || true
    docker network rm vote-net 2>/dev/null || true
    
    print_step "Creating custom Docker network..."
    docker network create vote-net
    print_success "Custom network 'vote-net' created"
    
    print_step "Starting Redis in the custom network..."
    docker run -d --name redis-server --network vote-net redis:alpine
    print_success "Redis started in vote-net network"
    
    print_step "Starting app in the same network..."
    docker run -d --name vote-app --network vote-net -p 5000:5000 -e REDIS_HOST=redis-server vote-app
    print_success "App started in vote-net network"
    
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        print_info "Testing voting functionality..."
        
        if test_voting; then
            print_success "🎉 VOTING WORKS! The magic of Docker networking!"
            print_info "Success Learning Points:"
            echo "   • Custom Docker networks enable container communication"
            echo "   • Hostname resolution works within the same network"
            echo "   • This is how microservices communicate in Docker"
            echo "   • Real-world applications use this pattern daily"
        else
            print_error "Voting still doesn't work (unexpected)"
        fi
        
        print_step "Testing network connectivity..."
        if docker exec vote-app python -c "import socket; socket.create_connection(('redis-server', 6379), timeout=5)" 2>/dev/null; then
            print_success "✅ Network connectivity: App can reach Redis on port 6379"
        else
            print_error "❌ Network connectivity: App cannot reach Redis on port 6379"
        fi
        
        print_step "Testing Redis application connectivity..."
        if docker exec vote-app python -c "import redis; r = redis.Redis(host='redis-server', port=6379, decode_responses=True); r.ping()" 2>/dev/null; then
            print_success "✅ Redis connectivity: App can connect and ping Redis"
        else
            print_error "❌ Redis connectivity: App cannot connect to Redis"
        fi
    else
        print_error "App is not responding"
    fi
    
    sleep 3
    
    # Final summary
    print_header "🎉 Demo Complete!"
    echo -e "${GREEN}Congratulations! You've experienced Docker networking magic!${NC}"
    echo ""
    print_info "What you learned:"
    echo "   ✅ Container isolation and communication"
    echo "   ✅ Docker network concepts"
    echo "   ✅ How to fix common networking issues"
    echo "   ✅ Real-world microservices patterns"
    echo ""
    print_info "Key takeaways:"
    echo "   • Containers need explicit network configuration"
    echo "   • Custom networks enable service communication"
    echo "   • This pattern is used in production every day"
    echo "   • Docker networking is powerful but requires understanding"
    echo ""
    print_step "Final cleanup..."
    cleanup
    print_success "Demo completed successfully!"
    echo ""
    echo -e "${CYAN}Thanks for experiencing Docker Networking Magic! 🚀${NC}"
    echo ""
    print_info "To run the interactive demo with explanations:"
    echo "   ./demo_manual.sh"
    echo ""
    print_info "To make the app public:"
    echo "   ./scripts/expose_ngrok.sh"
    echo "   ./scripts/expose_cloudflared.sh"
}

# Check if we're in the right directory
if [[ ! -f "app/app.py" ]]; then
    print_error "Please run this script from the scenario_03_networking directory"
    exit 1
fi

# Make scripts executable
chmod +x scripts/*.sh

# Run the demo
run_demo 