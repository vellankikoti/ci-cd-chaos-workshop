#!/bin/bash
# 🎓 Docker Image Scanner - Unforgettable Learning Experience
# Interactive workshop demo script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${PURPLE}🎓 $1${NC}"
}

print_step() {
    echo -e "${BLUE}📝 Step $1:${NC} $2"
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

print_info() {
    echo -e "${CYAN}💡 $1${NC}"
}

# Clear screen and show welcome
clear
echo -e "${PURPLE}"
echo "🐳 Docker Image Scanner - Unforgettable Learning Experience"
echo "=========================================================="
echo -e "${NC}"

print_header "Welcome to the Docker Security Workshop!"
echo ""
print_info "This workshop will teach you:"
echo "   • Real Docker image building and analysis"
echo "   • Security vulnerability detection with Trivy"
echo "   • Best practices for secure Docker images"
echo "   • Industry-standard security scanning"
echo ""

# Step 1: Environment Setup
print_step "1" "Setting up the environment"
echo ""

print_info "Checking prerequisites..."
if ! docker ps > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop first."
    exit 1
fi
print_success "Docker is running"

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the correct directory."
    exit 1
fi
print_success "requirements.txt found"

# Step 2: Validation
print_step "2" "Validating Docker build functionality"
echo ""

print_info "Running build validation tests..."
if ./validate_docker_build.sh; then
    print_success "All build tests passed!"
else
    print_error "Build validation failed. Please check the errors above."
    exit 1
fi

# Step 3: Start the Application
print_step "3" "Starting the Docker Image Scanner"
echo ""

print_info "Starting the application on http://localhost:8000"
print_info "The application will be available in your browser"
echo ""

# Check if Python is available
if ! python --version > /dev/null 2>&1; then
    print_error "Python is not available. Please install Python 3.8+"
    exit 1
fi

print_info "Installing Python dependencies..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    print_success "Dependencies installed"
else
    print_warning "Some dependencies may not be installed. Continuing anyway..."
fi

echo ""
print_header "🚀 Starting the Application..."
echo ""
print_info "The application will start in the background."
print_info "You can access it at: http://localhost:8000"
echo ""
print_info "Press Ctrl+C to stop the application when done."
echo ""

# Start the application in background
python app.py &
APP_PID=$!

# Wait a moment for the app to start
sleep 3

# Check if the app is running
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    print_success "Application is running successfully!"
else
    print_warning "Application may still be starting up..."
fi

echo ""
print_header "🎯 Workshop Activities"
echo ""
print_info "Now you can perform these activities:"
echo ""
echo "1. 📊 Analyze Pre-built Images:"
echo "   • nginx:1.25-alpine (secure)"
echo "   • python:3.8 (vulnerable)"
echo "   • node:18-alpine (modern)"
echo ""
echo "2. 🔍 Compare Security Results:"
echo "   • Compare secure vs vulnerable images"
echo "   • Analyze vulnerability differences"
echo "   • Learn best practices"
echo ""
echo "4. 📚 Educational Insights:"
echo "   • Read the security recommendations"
echo "   • Understand vulnerability types"
echo "   • Learn industry benchmarks"
echo ""

print_header "🎓 Learning Objectives"
echo ""
print_info "By the end of this workshop, you will understand:"
echo "   • How Docker images are built and analyzed"
echo "   • Real security vulnerabilities in container images"
echo "   • Best practices for secure Docker images"
echo "   • Industry-standard security scanning tools"
echo "   • How to interpret security scan results"
echo ""

print_header "🔧 Troubleshooting"
echo ""
print_info "If you encounter issues:"
echo "   • Ensure Docker Desktop is running"
echo "   • Check that port 8000 is available"
echo "   • Verify Trivy is installed (brew install trivy)"
echo "   • Restart the application if needed"
echo ""

# Wait for user to finish
echo ""
print_header "🎉 Workshop Ready!"
echo ""
print_info "The application is running and ready for your Docker security workshop!"
print_info "Open your browser and navigate to: http://localhost:8000"
echo ""
print_info "Press Ctrl+C when you're done to stop the application."
echo ""

# Wait for interrupt signal
trap "echo ''; print_info 'Stopping application...'; kill $APP_PID 2>/dev/null; print_success 'Workshop completed!'; exit 0" INT

# Keep the script running
while true; do
    sleep 1
done 