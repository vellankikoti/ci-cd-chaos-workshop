#!/bin/bash

# Docker Image Scanner - Manual Demo Script
# Walks through 5 different security scenarios seamlessly

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
CYAN='\033[0;36m'
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

print_info() {
    echo -e "${CYAN}💡 $1${NC}"
}

wait_for_user() {
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read -r
    echo ""
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
    print_header "Starting Docker Image Scanner Application"
    echo "=============================================="
    
    # Check if app is already running
    if check_app_running; then
        print_success "Application is already running on http://localhost:8000"
        return 0
    fi
    
    print_step "Starting the Docker Image Scanner application..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not available. Please install Python 3.8+"
        exit 1
    fi
    
    # Check if requirements are installed
    if ! python3 -c "import fastapi" 2>/dev/null; then
        print_warning "Installing Python dependencies..."
        pip3 install -r requirements.txt > /dev/null 2>&1 || print_warning "Some dependencies may not be installed"
    fi
    
    # Start the application in background
    print_step "Starting application on http://localhost:8000..."
    python3 app.py > app.log 2>&1 &
    APP_PID=$!
    
    # Wait for application to start
    print_step "Waiting for application to start..."
    local attempts=0
    while [ $attempts -lt 30 ]; do
        if check_app_running; then
            print_success "Application is running successfully!"
            break
        fi
        echo -n "."
        sleep 2
        attempts=$((attempts + 1))
    done
    
    if [ $attempts -eq 30 ]; then
        print_error "Application failed to start. Check app.log for details."
        exit 1
    fi
    
    echo ""
    print_success "🎉 Docker Image Scanner is ready!"
    print_step "Open your browser to: http://localhost:8000"
    echo ""
}

# Function to run a scenario
run_scenario() {
    local scenario_num=$1
    local scenario_name=$2
    local scenario_desc=$3
    local demo_instructions=$4
    
    print_header "SCENARIO $scenario_num: $scenario_name"
    echo "=============================================="
    echo ""
    echo "$scenario_desc"
    echo ""
    
    print_info "Demo Instructions:"
    echo "$demo_instructions"
    echo ""
    
    print_step "Ready to explore $scenario_name..."
    print_step "Application is running at: http://localhost:8000"
    print_step "Follow the instructions above to explore this scenario"
    
    wait_for_user
}

# Function to validate environment
validate_environment() {
    print_header "Environment Validation"
    echo "========================"
    
    # Check Docker
    print_step "Checking Docker..."
    if ! docker ps > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_success "Docker is running"

    # Check Docker socket
    print_step "Checking Docker socket..."
    if [ ! -S "/var/run/docker.sock" ]; then
        print_error "Docker socket not found at /var/run/docker.sock. Trivy scanning will not work."
        exit 1
    fi
    print_success "Docker socket is available"

    # Check Python
    print_step "Checking Python..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not available"
        exit 1
    fi
    print_success "Python3 is available"

    # Check requirements
    print_step "Checking requirements..."
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    print_success "Requirements file found"

    echo ""
    print_success "Environment validation complete! (Trivy will be run via Docker image)"
    echo ""
}

# Function to show educational content
show_educational_content() {
    local scenario_num=$1
    local content=$2
    
    echo ""
    print_header "🎓 EDUCATIONAL CONTENT - Scenario $scenario_num"
    echo "=================================================="
    echo "$content"
    echo ""
}

# Main demo
main() {
    print_header "🐳 Docker Image Scanner - Interactive Demo"
    echo "==============================================="
    echo ""
    echo "This interactive demo will walk through 4 different Docker security scenarios:"
    echo "1. Secure Image Analysis - Understanding best practices"
    echo "2. Vulnerable Image Analysis - Learning from security issues"
    echo "3. Image Comparison - Side-by-side security analysis"
    echo "4. Real-World Application - Production security scanning"
    echo ""
    echo "Each scenario will help you explore different aspects of Docker security"
    echo "and provide hands-on educational insights."
    echo ""
    
    wait_for_user
    
    # Validate environment
    validate_environment
    
    # Start the application
    start_application
    
    # Scenario 1: Secure Image Analysis
    run_scenario 1 "Secure Image Analysis" \
        "We'll analyze secure, well-maintained Docker images to understand what makes an image secure. We'll look at Alpine-based images and modern Python images that follow security best practices." \
        "1. Open http://localhost:8000 in your browser
2. Enter 'nginx:1.25-alpine' in the image field
3. Click 'Analyze Image'
4. You'll see:
   • Low vulnerability count
   • High security score
   • Best practices recommendations
   • Educational insights
5. Then try 'python:3.11-slim' for comparison
6. Notice why Alpine images are more secure"
    
    show_educational_content 1 \
        "This scenario teaches us about secure base image selection. Alpine Linux images are minimal, 
have a small attack surface, and are regularly updated. We'll see:
• How base image choice affects security
• The importance of minimal attack surface
• Security score interpretation
• Best practices for image selection
• Real vulnerability data from Trivy"

    # Scenario 2: Vulnerable Image Analysis
    run_scenario 2 "Vulnerable Image Analysis" \
        "We'll analyze images with known vulnerabilities to understand security risks and learn how to identify and address security issues in Docker images." \
        "1. Enter 'python:3.8' in the image field
2. Click 'Analyze Image'
3. You'll see:
   • Higher vulnerability count
   • Lower security score
   • Specific CVE details
   • Severity levels (Critical, High, Medium, Low)
   • Remediation recommendations
4. Compare with the secure images from Scenario 1
5. Notice the importance of regular updates"
    
    show_educational_content 2 \
        "This scenario demonstrates real security vulnerabilities in Docker images. We'll learn:
• How to interpret vulnerability reports
• Understanding CVE severity levels
• The impact of outdated base images
• Security remediation strategies
• Why regular updates are crucial
• Real-world security implications"

    # Scenario 3: Image Comparison
    run_scenario 3 "Image Comparison" \
        "We'll compare multiple images side-by-side to understand security trade-offs and learn how to make informed decisions about image selection." \
        "1. Click the 'Compare Images' tab
2. Enter 'python:3.8' and 'python:3.11-slim' for comparison
3. You'll see:
   • Side-by-side vulnerability comparison
   • Security score differences
   • Best practices analysis
   • Recommendations for improvement
4. Try comparing 'nginx:1.25-alpine' vs 'ubuntu:22.04'
5. Notice the security implications of different base images"
    
    show_educational_content 3 \
        "This scenario teaches comparative security analysis. We'll learn:
• How to compare security metrics between images
• Understanding security trade-offs
• Making informed image selection decisions
• Security vs functionality considerations
• Industry benchmarking
• Risk assessment strategies"

    # Scenario 4: Real-World Application
    run_scenario 4 "Real-World Application" \
        "We'll demonstrate how to integrate Docker security scanning into real-world workflows and show production-ready security practices." \
        "1. Explore the comprehensive analysis results
2. Learn how to interpret detailed reports
3. Review educational insights and learning recommendations
4. Understand integration with CI/CD pipelines
5. See how to use this for team education
6. Experience the WebSocket real-time updates
7. Try the comparison features for team decision-making"
    
    show_educational_content 4 \
        "This scenario demonstrates production-ready Docker security practices. We'll learn:
• How to integrate security scanning into CI/CD
• Team education and security awareness
• Production security monitoring
• Compliance and audit requirements
• Real-time security feedback
• Automated security workflows
• Best practices for enterprise environments"

    # Final summary
    print_header "🎉 Demo Complete!"
    echo "=================="
    echo ""
    print_success "You've successfully explored Docker security analysis!"
    echo ""
    echo "What you've learned:"
    echo "• Scenario 1: Secure image analysis and best practices"
    echo "• Scenario 2: Vulnerability identification and remediation"
    echo "• Scenario 3: Comparative security analysis"
    echo "• Scenario 4: Real-world security integration"
    echo ""
    print_info "Key takeaways:"
    echo "• Docker security is critical for production environments"
    echo "• Regular vulnerability scanning is essential"
    echo "• Base image selection significantly impacts security"
    echo "• Security scanning can be integrated into CI/CD"
    echo "• Education and awareness are key to security"
    echo ""
    print_step "The application is still running at http://localhost:8000"
    print_step "You can continue exploring or try additional features"
    echo ""
    print_warning "To stop the application, press Ctrl+C or run: pkill -f 'python3 app.py'"
}

# Cleanup function
cleanup() {
    echo ""
    print_step "Cleaning up..."
    pkill -f "python3 app.py" 2>/dev/null || true
    print_success "Demo completed successfully!"
}

# Set up trap for cleanup
trap cleanup EXIT

# Run the demo
main 