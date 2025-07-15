#!/bin/bash
# 🐳 Docker Image Scanner - Build Validation Script
# Tests Docker build functionality and provides educational insights

set -e

echo "🚀 Docker Image Scanner - Build Validation"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
print_status "Checking Docker availability..."
if ! docker ps > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    echo ""
    echo "💡 To start Docker:"
    echo "   • macOS: Open Docker Desktop app"
    echo "   • Linux: sudo systemctl start docker"
    echo "   • Windows: Start Docker Desktop"
    exit 1
fi
print_success "Docker is running"

# Check if requirements.txt exists
print_status "Checking for requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in current directory"
    exit 1
fi
print_success "requirements.txt found"

# Test 1: Simple Dockerfile (no requirements.txt)
print_status "Test 1: Building simple Dockerfile..."
cat > test_simple.dockerfile << 'EOF'
FROM alpine:3.18
CMD ["echo", "Hello from Alpine!"]
EOF

if docker build -f test_simple.dockerfile -t test-simple .; then
    print_success "Simple Dockerfile build successful"
    docker rmi test-simple > /dev/null 2>&1
else
    print_error "Simple Dockerfile build failed"
    rm -f test_simple.dockerfile
    exit 1
fi

# Test 2: Dockerfile with requirements.txt
print_status "Test 2: Building Dockerfile with requirements.txt..."
cat > test_requirements.dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements_docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-c", "print('Build test successful!')"]
EOF

if docker build -f test_requirements.dockerfile -t test-requirements .; then
    print_success "Dockerfile with requirements.txt build successful"
    docker rmi test-requirements > /dev/null 2>&1
else
    print_error "Dockerfile with requirements.txt build failed"
    rm -f test_requirements.dockerfile
    exit 1
fi

# Test 3: Vulnerable Dockerfile for educational purposes
print_status "Test 3: Building vulnerable Dockerfile for security testing..."
cat > test_vulnerable.dockerfile << 'EOF'
FROM python:3.8
WORKDIR /app
RUN pip install flask==2.0.1
USER root
CMD ["python", "-c", "print('Vulnerable app running!')"]
EOF

if docker build -f test_vulnerable.dockerfile -t test-vulnerable .; then
    print_success "Vulnerable Dockerfile build successful (for security testing)"
    docker rmi test-vulnerable > /dev/null 2>&1
else
    print_warning "Vulnerable Dockerfile build failed (this is expected for security testing)"
fi

# Cleanup
rm -f test_simple.dockerfile test_requirements.dockerfile test_vulnerable.dockerfile

echo ""
echo "🎉 All validation tests passed!"
echo ""
echo "📚 Educational Insights:"
echo "   • Test 1: Simple Dockerfile - No external dependencies"
echo "   • Test 2: Requirements.txt - Real-world Python app pattern"
echo "   • Test 3: Vulnerable Dockerfile - Security testing example"
echo ""
echo "🚀 Docker build functionality is ready for the workshop!"
echo ""
echo "💡 Workshop Tips:"
echo "   • Compare secure vs vulnerable base images"
echo "   • Analyze real-world patterns in your Dockerfiles"
echo ""
echo "🔍 Next Steps:"
echo "   1. Start the application: python app.py"
echo "   2. Open browser: http://localhost:8000" 