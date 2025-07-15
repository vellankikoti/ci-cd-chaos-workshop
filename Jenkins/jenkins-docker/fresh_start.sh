#!/bin/bash

# 🧹 Fresh Start Script for Jenkins CI/CD Chaos Workshop
# This script completely removes Jenkins data and starts fresh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo -e "${BLUE}🧹 Fresh Start - Jenkins CI/CD Chaos Workshop${NC}"
echo "=================================================="

# Stop and remove Jenkins container
print_info "Stopping and removing Jenkins container..."
docker stop jenkins 2>/dev/null || true
docker rm jenkins 2>/dev/null || true
print_status "Jenkins container removed"

# Remove Docker volumes (this deletes ALL Jenkins data)
print_info "Removing Jenkins volumes (this will delete ALL Jenkins data)..."
docker volume rm jenkins_home jenkins_workspace 2>/dev/null || true
print_status "Jenkins volumes removed"

# Clean up any chaos-app containers
print_info "Cleaning up any chaos-app containers..."
docker ps -a --filter "name=chaos-app-v" -q | xargs -r docker rm -f 2>/dev/null || true
print_status "Chaos app containers cleaned up"

print_status "Fresh start completed!"
echo ""
print_info "Now run: ./workshop_setup.sh"
echo "" 