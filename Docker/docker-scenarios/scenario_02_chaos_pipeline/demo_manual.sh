#!/bin/bash

# Manual Step-by-Step Demo Script
# This gives you complete control over each step

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

wait_for_user() {
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read -r
    echo ""
}

# Function to run a step
run_step() {
    local step=$1
    local port=$2
    local step_name=$3
    local step_dir=$4
    
    print_header "STEP $step: $step_name"
    echo "=========================================="
    
    # Clean up existing container for this step if it exists
    local container_name="chaos-step$step-$(echo $step_name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    print_step "Checking for existing container..."
    if docker ps -a --format "table {{.Names}}" | grep -q "^$container_name$"; then
        print_step "Found existing container, cleaning up..."
        docker stop "$container_name" 2>/dev/null || true
        docker rm "$container_name" 2>/dev/null || true
        print_success "Existing container cleaned up"
    fi
    
    # Clean up previous step if exists
    if [ $step -gt 1 ]; then
        local prev_step=$((step - 1))
        local prev_step_name=""
        case $prev_step in
            1) prev_step_name="fail-network" ;;
            2) prev_step_name="fail-resource" ;;
            3) prev_step_name="fail-service" ;;
            4) prev_step_name="fail-db" ;;
        esac
        
        if [ -n "$prev_step_name" ]; then
            print_step "Cleaning up previous step..."
            local prev_container_name="chaos-step$prev_step-$prev_step_name"
            docker stop "$prev_container_name" 2>/dev/null || true
            docker rm "$prev_container_name" 2>/dev/null || true
            print_success "Previous step cleaned up"
        fi
    fi
    
    # Build the container
    print_step "Building Docker image for $step_name..."
    cd scenarios/$step_dir/
    docker build -t chaos-step$step-$(echo $step_name | tr ' ' '-' | tr '[:upper:]' '[:lower:]') .
    cd ../../
    print_success "Docker image built successfully"
    
    # Start the service
    print_step "Starting $step_name service on port $port..."
    local image_name="chaos-step$step-$(echo $step_name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
    
    if [ "$step" = "2" ]; then
        # Step 2 needs memory limits
        docker run -d --name "$container_name" -p $port:8080 \
            --memory=128m --memory-swap=128m "$image_name"
    else
        docker run -d --name "$container_name" -p $port:8080 "$image_name"
    fi
    print_success "Service started"
    
    # Wait for service to be ready
    print_step "Waiting for service to be ready..."
    local attempts=0
    while [ $attempts -lt 30 ]; do
        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            print_success "Service is ready!"
            break
        fi
        echo -n "."
        sleep 2
        attempts=$((attempts + 1))
    done
    
    if [ $attempts -eq 30 ]; then
        if [ "$step" = "2" ]; then
            print_warning "Service was killed by OOM (Out of Memory) - This is EXPECTED for Step 2!"
            print_step "This demonstrates resource failure - the container exceeded its 128MB memory limit"
            print_step "Let's restart it to show the educational content..."
            
            # Restart the container for step 2
            docker start "$container_name" 2>/dev/null || true
            sleep 5
            
            # Try one more health check
            if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
                print_success "Service restarted and is responding!"
            else
                print_step "Service is designed to fail - this demonstrates resource limitations"
            fi
        else
        print_step "Service took longer than expected to start"
        fi
    fi
    
    echo ""
    print_step "Service is now running at: http://localhost:$port"
    print_step "Health check: http://localhost:$port/health"
    print_step "Debug info: http://localhost:$port/debug"
    if [ "$step" = "2" ]; then
        print_step "Educational experiment: http://localhost:$port/run-experiment-educational"
        print_step "Safe experiment: http://localhost:$port/run-experiment-safe"
        print_step "Run experiment (kills container): http://localhost:$port/run-experiment"
    else
    print_step "Run experiment: http://localhost:$port/run-experiment"
    fi
    
    wait_for_user
}

# Main demo
main() {
    print_header "Manual Chaos Engineering Demo"
    echo "=================================="
    echo ""
    echo "This demo will run each step manually, allowing you to explain everything."
    echo "Each step will build, start, and show you the service endpoints."
    echo "You can then explain what's happening and show the audience."
    echo ""
    
    wait_for_user
    
    # Step 1: Network Failure
    run_step 1 8081 "Network Failure" "step1_fail_network"
    
    echo "🎓 EDUCATIONAL CONTENT - Step 1:"
    echo "I've built this service to demonstrate network connectivity challenges."
    echo "It tries to connect to external services like DNS, HTTP, and internal"
    echo "services that don't exist. The service will fail because it can't reach dependencies."
    echo ""
    echo "🎯 What I'm going to show you:"
    echo "• Health endpoint: curl http://localhost:8081/health"
    echo "• Debug info: curl http://localhost:8081/debug"
    echo "• Run experiment: curl http://localhost:8081/run-experiment"
    
    wait_for_user
    
    # Step 2: Resource Failure
    run_step 2 8082 "Resource Failure" "step2_fail_resource"
    
    echo "🎓 EDUCATIONAL CONTENT - Step 2:"
    echo "I've built this service to demonstrate real image processing challenges."
    echo "It creates large images that consume significant memory, and I've set"
    echo "memory limits to 128MB to show you what happens when containers exceed limits."
    echo ""
    echo "🎯 DEMONSTRATION ORDER (IMPORTANT):"
    echo "1. First, I'll show you the educational content (container survives):"
    echo "   • curl http://localhost:8082/run-experiment-educational"
    echo "   • curl http://localhost:8082/run-experiment-safe"
    echo "   • curl http://localhost:8082/debug"
    echo "   • curl http://localhost:8082/process-image/1024/1024"
    echo ""
    echo "2. Finally, I'll demonstrate the full OOM experience (kills container):"
    echo "   • curl http://localhost:8082/run-experiment"
    echo ""
    echo "💡 This order ensures we learn everything before the container gets terminated!"
    
    wait_for_user
    
    # Step 3: Service Failure
    run_step 3 8083 "Service Failure" "step3_fail_service"
    
    echo "📚 EDUCATIONAL CONTENT - Step 3:"
    echo "This service manages user sessions. It tries to connect to Redis for"
    echo "session storage, but Redis isn't running. The service will fail but"
    echo "provides fallback mechanisms."
    echo ""
    echo "What to show the audience:"
    echo "• Health endpoint: curl http://localhost:8083/health"
    echo "• Debug info: curl http://localhost:8083/debug"
    echo "• Session creation: curl http://localhost:8083/session/create"
    echo "• Run experiment: curl http://localhost:8083/run-experiment"
    
    wait_for_user
    
    # Step 4: Database Failure
    run_step 4 8084 "Database Failure" "step4_fail_db"
    
    echo "🗄️ EDUCATIONAL CONTENT - Step 4:"
    echo "This service manages users and tries to connect to MySQL database."
    echo "MySQL isn't running, so it will fail, but it demonstrates how"
    echo "applications handle database dependencies."
    echo ""
    echo "What to show the audience:"
    echo "• Health endpoint: curl http://localhost:8084/health"
    echo "• Debug info: curl http://localhost:8084/debug"
    echo "• User creation: curl -X POST http://localhost:8084/user/create"
    echo "• Run experiment: curl http://localhost:8084/run-experiment"
    
    wait_for_user
    
    # Step 5: Success with Real Services
    print_header "STEP 5: Success with Real Services"
    echo "=========================================="
    
    print_step "Setting up production-ready system with Redis and MySQL..."
    
    # Clean up previous step
    docker stop chaos-step4-fail-db 2>/dev/null || true
    docker rm chaos-step4-fail-db 2>/dev/null || true
    
    # Start the production system with docker-compose
    print_step "Starting production system with docker-compose..."
    cd scenarios/step5_success
    docker-compose up -d --build
    cd ../..
    
    print_step "Waiting for services to be ready..."
    sleep 30
    
    print_success "Production system is running!"
    echo ""
    print_step "Services available:"
    print_step "• Main app: http://localhost:8085"
    print_step "• Health check: http://localhost:8085/health"
    print_step "• Debug info: http://localhost:8085/debug"
    print_step "• Metrics: http://localhost:8085/metrics"
    print_step "• Run experiment: http://localhost:8085/run-experiment"
    print_step "• Redis: localhost:6379"
    print_step "• MySQL: localhost:3306"
    
    echo ""
    echo "🎉 EDUCATIONAL CONTENT - Step 5:"
    echo "This is a production-ready system with all the best practices:"
    echo "• Comprehensive health monitoring"
    echo "• Proper error handling and fallback mechanisms"
    echo "• Real database persistence with MySQL"
    echo "• Session management with Redis"
    echo "• Metrics and observability"
    echo "• Resilience patterns"
    
    wait_for_user
    
    # Final cleanup
    print_header "Demo Complete!"
    echo "=================="
    echo ""
    print_step "Cleaning up all containers..."
    cd scenarios/step5_success
    docker-compose down 2>/dev/null || true
    cd ../..
    docker stop $(docker ps -q --filter "name=chaos-step") 2>/dev/null || true
    docker rm $(docker ps -aq --filter "name=chaos-step") 2>/dev/null || true
    print_success "All containers cleaned up"
    
    echo ""
    print_success "🎓 Progressive Chaos Engineering Demo completed successfully!"
    echo ""
    echo "What we learned:"
    echo "• Step 1: Network connectivity challenges"
    echo "• Step 2: Resource management and memory limits"
    echo "• Step 3: Service dependencies and fallback mechanisms"
    echo "• Step 4: Database connectivity and error handling"
    echo "• Step 5: Production-ready, resilient microservices architecture"
}

# Run the demo
main
