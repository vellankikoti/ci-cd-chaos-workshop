#!/bin/bash

# 🚀 Docker Networking Magic - Interactive Demo Script
# ====================================================
# This script provides a step-by-step, educational experience
# demonstrating Docker networking concepts through a voting app.

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

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to wait for user input
wait_for_user() {
    if [ "${NON_INTERACTIVE:-false}" != "true" ]; then
        echo -e "\n${YELLOW}Press Enter to continue...${NC}"
        read -r
    else
        echo -e "\n${YELLOW}Continuing automatically...${NC}"
        sleep 2
    fi
}

# Function to test app endpoint
test_app_endpoint() {
    local url="http://localhost:5000"
    local max_attempts=30
    local attempt=1
    
    print_step "Testing app endpoint..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "App is responding at $url"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "App is not responding after $max_attempts attempts"
    return 1
}

# Function to test voting functionality
test_voting() {
    print_step "Testing voting functionality..."
    
    # Get initial vote count
    local initial_response=$(curl -s http://localhost:5000)
    local initial_count=$(echo "$initial_response" | awk '/WFH Votes/{getline; print}' | grep -o '[0-9]\+' | head -1 || echo "0")
    
    print_info "Initial WFH votes: $initial_count"
    
    # Submit a vote
    local response=$(curl -s -X POST -d "vote=wfh" http://localhost:5000)
    
    if echo "$response" | grep -q "Voting Failed!"; then
        print_success "Voting failed as expected - no Redis connection!"
        return 1
    elif echo "$response" | grep -q "Vote Recorded Successfully!"; then
        # Wait a moment for the vote to be processed
        sleep 2
        
        # Get the new vote count
        local new_response=$(curl -s http://localhost:5000)
        local new_count=$(echo "$new_response" | awk '/WFH Votes/{getline; print}' | grep -o '[0-9]\+' | head -1 || echo "0")
        
        print_info "New WFH votes: $new_count"
        
        # Ensure we have valid numbers
        if [[ "$initial_count" =~ ^[0-9]+$ ]] && [[ "$new_count" =~ ^[0-9]+$ ]]; then
            if [ "$new_count" -gt "$initial_count" ]; then
                print_success "✅ Vote was recorded successfully in Redis!"
                return 0
            else
                print_error "❌ Vote was not recorded (count didn't increase)"
                return 1
            fi
        else
            print_error "❌ Invalid vote counts detected"
            return 1
        fi
    else
        print_error "Could not determine app status"
        return 1
    fi
}

# Function to show container status
show_container_status() {
    print_step "Container Status:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(vote-app|redis-server)" || echo "No containers running"
    echo ""
}

# Function to show network status
show_network_status() {
    print_step "Network Status:"
    docker network ls | grep vote-net || echo "vote-net network not found"
    echo ""
}

# Function to cleanup
cleanup() {
    print_step "Cleaning up containers and networks..."
    docker rm -f vote-app redis-server 2>/dev/null || true
    docker network rm vote-net vote-net1 vote-net2 2>/dev/null || true
    print_success "Cleanup completed"
}

# Main demo function
run_demo() {
    print_header "🚀 Docker Networking Magic - Interactive Demo"
    echo -e "${CYAN}This demo will show you the magic of Docker networking${NC}"
    echo -e "${CYAN}through a real voting application with Redis.${NC}"
    echo ""
    print_info "We'll demonstrate:"
    echo "  1. Running an app without a database (failure)"
    echo "  2. Adding a database in the wrong network (failure)"
    echo "  3. Fixing the network (success!)"
    echo "  4. Complete working system with all concepts"
    echo ""
    print_info "This will teach you:"
    echo "  • How Docker networks work"
    echo "  • Why containers need proper networking"
    echo "  • How to fix common networking issues"
    echo "  • Real-world microservices patterns"
    echo ""
    wait_for_user
    
    # Initial cleanup
    print_header "🧹 Initial Cleanup"
    cleanup
    wait_for_user
    
    # Step 1: Run app without database
    print_header "🔴 STEP 1: App Without Database (Expected Failure)"
    echo -e "${YELLOW}Let's start by running our voting app without any database.${NC}"
    echo -e "${YELLOW}This will demonstrate what happens when containers can't communicate.${NC}"
    echo ""
    
    # Check if port 5000 is available
    if ! check_port 5000; then
        print_warning "Port 5000 is already in use. Cleaning up..."
        cleanup
        sleep 2
    fi
    
    print_step "Building the Flask voting app..."
    if docker build -t vote-app ./app; then
        print_success "App built successfully"
    else
        print_error "Failed to build app"
        exit 1
    fi
    
    print_step "Running app without Redis database..."
    if docker run -d --name vote-app -p 5000:5000 vote-app; then
        print_success "App container started"
    else
        print_error "Failed to start app container"
        exit 1
    fi
    
    # Wait for app to be ready
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        echo ""
        print_info "🎯 Educational Moment:"
        echo "   • The app starts successfully"
        echo "   • But it has no database to store votes"
        echo "   • When you try to vote, it will fail"
        echo ""
        print_step "Let's test what happens when we try to vote..."
        
        if test_voting; then
            print_warning "Voting worked (unexpected in this scenario)"
        else
            print_success "Voting failed as expected - no database connection!"
        fi
        
        echo ""
        print_info "💡 What we learned:"
        echo "   • Containers are isolated by default"
        echo "   • Apps need explicit database connections"
        echo "   • No automatic service discovery"
        echo ""
        wait_for_user
    else
        print_error "App is not responding"
        exit 1
    fi
    
    # Step 2: Add database in wrong network
    print_header "🔴 STEP 2: Database in Wrong Network (Expected Failure)"
    echo -e "${YELLOW}Now let's add a Redis database, but put it in a different network.${NC}"
    echo -e "${YELLOW}This will show how Docker networks isolate containers.${NC}"
    echo ""
    
    print_step "Stopping the previous app..."
    docker stop vote-app 2>/dev/null || true
    docker rm vote-app 2>/dev/null || true
    
    print_step "Starting Redis database..."
    if docker run -d --name redis-server redis:alpine; then
        print_success "Redis container started"
    else
        print_error "Failed to start Redis container"
        exit 1
    fi
    
    print_step "Starting app with Redis hostname..."
    if docker run -d --name vote-app -p 5000:5000 -e REDIS_HOST=redis-server vote-app; then
        print_success "App container started"
    else
        print_error "Failed to start app container"
        exit 1
    fi
    
    # Wait for app to be ready
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        echo ""
        print_info "🎯 Educational Moment:"
        echo "   • Both containers are running"
        echo "   • App tries to connect to Redis by hostname"
        echo "   • But they're in different networks"
        echo "   • Hostname resolution fails"
        echo ""
        print_step "Let's test voting again..."
        
        if test_voting; then
            print_warning "Voting worked (unexpected in this scenario)"
        else
            print_success "Voting failed as expected - network isolation!"
        fi
        
        echo ""
        print_info "💡 What we learned:"
        echo "   • Docker networks isolate containers"
        echo "   • Containers in different networks can't see each other"
        echo "   • Need explicit network configuration"
        echo ""
        wait_for_user
    else
        print_error "App is not responding"
        exit 1
    fi
    
    # Step 3: Fix the network
    print_header "🟢 STEP 3: Fix the Network (Success!)"
    echo -e "${YELLOW}Now let's create a custom network and put both containers in it.${NC}"
    echo -e "${YELLOW}This will demonstrate proper container communication.${NC}"
    echo ""
    
    print_step "Cleaning up previous containers..."
    docker stop vote-app redis-server 2>/dev/null || true
    docker rm vote-app redis-server 2>/dev/null || true
    
    print_step "Creating custom Docker network..."
    if docker network create vote-net; then
        print_success "Custom network 'vote-net' created"
    else
        print_error "Failed to create network"
        exit 1
    fi
    
    print_step "Starting Redis in the custom network..."
    if docker run -d --name redis-server --network vote-net redis:alpine; then
        print_success "Redis container started in vote-net"
    else
        print_error "Failed to start Redis container"
        exit 1
    fi
    
    print_step "Starting app in the same network..."
    if docker run -d --name vote-app --network vote-net -p 5000:5000 -e REDIS_HOST=redis-server vote-app; then
        print_success "App started in vote-net network"
    else
        print_error "Failed to start app in network"
        exit 1
    fi
    
    # Wait for app to be ready
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "App is accessible at http://localhost:5000"
        echo ""
        print_info "🎯 Educational Moment:"
        echo "   • Both containers are in the same network"
        echo "   • Hostname resolution works"
        echo "   • Voting functionality should work perfectly"
        echo ""
        print_step "Let's test voting functionality..."
        
        if test_voting; then
            print_success "🎉 Voting works perfectly!"
            echo ""
            print_info "💡 What we learned:"
            echo "   • Custom networks enable container communication"
            echo "   • Hostname resolution within same network"
            echo "   • This is how microservices communicate"
            echo "   • Real-world pattern used daily"
            echo ""
        else
            print_error "Voting still failed (unexpected)"
        fi
        
        wait_for_user
    else
        print_error "App is not responding"
        exit 1
    fi
    
    # Step 4: Complete working system with all concepts
    print_header "🎉 STEP 4: Complete Working System (Final Success!)"
    echo -e "${YELLOW}Now let's put everything together and create a complete, working system!${NC}"
    echo -e "${YELLOW}This demonstrates all the concepts working together in harmony.${NC}"
    echo ""
    
    print_step "Cleaning up previous containers and networks..."
    docker stop vote-app redis-server 2>/dev/null || true
    docker rm vote-app redis-server 2>/dev/null || true
    docker network rm vote-net 2>/dev/null || true
    
    print_step "Creating a production-ready network..."
    docker network create vote-net
    print_success "Created vote-net network"
    
    print_step "Starting Redis database in the network..."
    if docker run -d --name redis-server --network vote-net redis:alpine; then
        print_success "Redis container started in vote-net"
    else
        print_error "Failed to start Redis container"
        exit 1
    fi
    
    print_step "Starting the voting app with full configuration..."
    if docker run -d --name vote-app --network vote-net -p 5000:5000 -e REDIS_HOST=redis-server vote-app; then
        print_success "App container started with full configuration"
    else
        print_error "Failed to start app container"
        exit 1
    fi
    
    # Wait for app to be ready
    print_step "Waiting for app to be ready..."
    sleep 5
    
    if test_app_endpoint; then
        print_success "🎉 Complete system is running at http://localhost:5000"
        echo ""
        print_info "🎯 Final Educational Moment:"
        echo "   • Both containers are in the same network (vote-net)"
        echo "   • App can communicate with Redis (hostname resolution works)"
        echo "   • Port is published to host (accessible from your computer)"
        echo "   • This is a production-ready microservices setup!"
        echo ""
        print_step "Let's test the complete voting system..."
        
        if test_voting; then
            print_success "🎉 VOTING WORKS PERFECTLY! Complete system is functional!"
            echo ""
            print_info "💡 What we've achieved:"
            echo "   ✅ Container communication (app ↔ Redis)"
            echo "   ✅ Network configuration (custom Docker network)"
            echo "   ✅ Port publishing (host access)"
            echo "   ✅ Service discovery (hostname resolution)"
            echo "   ✅ Production-ready microservices architecture"
            echo ""
            print_info "🔧 Technical Summary:"
            echo "   • Network: vote-net (custom bridge network)"
            echo "   • Redis: redis-server:6379 (internal communication)"
            echo "   • App: localhost:5000 (host access)"
            echo "   • Communication: HTTP + Redis protocol"
            echo ""
            print_info "🌐 Real-world applications:"
            echo "   • This is how microservices communicate in production"
            echo "   • Database connectivity patterns"
            echo "   • Service discovery and networking"
            echo "   • Container orchestration concepts"
            echo ""
        else
            print_error "Voting failed in final step (unexpected)"
        fi
        
        echo ""
        print_step "Let's verify our complete system..."
        show_container_status
        show_network_status
        
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
        
        wait_for_user
    else
        print_error "Complete system is not responding"
        exit 1
    fi
    
    # Final summary
    print_header "🎉 Demo Complete!"
    echo -e "${GREEN}Congratulations! You've experienced the full Docker networking journey.${NC}"
    echo ""
    print_info "What you've learned:"
    echo "   ✅ Container isolation and communication"
    echo "   ✅ Docker networks and hostname resolution"
    echo "   ✅ How to fix common networking issues"
    echo "   ✅ Production-ready microservices architecture"
    echo ""
    print_info "Real-world applications:"
    echo "   • Microservices communication patterns"
    echo "   • Database connectivity in containers"
    echo "   • Network security and isolation"
    echo "   • Debugging container connectivity issues"
    echo "   • Production-ready container orchestration"
    echo ""
    print_info "🎯 Key Takeaways:"
    echo "   • Docker networks are powerful tools for container communication"
    echo "   • Proper network configuration is crucial for microservices"
    echo "   • Port publishing enables host access to containerized services"
    echo "   • Network isolation provides security boundaries"
    echo "   • Debugging skills are essential for container environments"
    echo ""
    print_step "Cleaning up..."
    cleanup
    print_success "Demo completed successfully!"
    echo ""
    echo -e "${CYAN}Your Docker networking skills are now production-ready! 🚀${NC}"
    echo -e "${CYAN}You can apply these concepts to real-world container deployments.${NC}"
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