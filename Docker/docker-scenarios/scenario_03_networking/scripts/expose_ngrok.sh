#!/bin/bash

# 🚀 Expose Voting App via ngrok
# ================================
# This script exposes the local voting app via ngrok for public access

set -e

# Color codes for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Exposing Voting App via ngrok...${NC}"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${YELLOW}⚠️  ngrok not found. Installing...${NC}"
    echo "Please install ngrok first:"
    echo "  brew install ngrok/ngrok/ngrok"
    echo ""
    echo "Or download from: https://ngrok.com/download"
    exit 1
fi

# Check if the app is running
if ! docker ps | grep -q vote-app; then
    echo -e "${YELLOW}⚠️  Voting app is not running.${NC}"
    echo "Please run the demo first:"
    echo "  ./demo_simple.sh"
    echo ""
    echo "Or start the app manually:"
    echo "  ./scripts/fix_network.sh"
    exit 1
fi

echo -e "${GREEN}✅ Voting app is running on port 5000${NC}"
echo ""
echo -e "${BLUE}🌐 Starting ngrok tunnel...${NC}"
echo "This will create a public URL that anyone can access!"
echo ""
echo -e "${YELLOW}📝 Note: The free ngrok plan has limitations:${NC}"
echo "  • URLs change each time you restart ngrok"
echo "  • Limited number of connections per minute"
echo "  • For production, consider ngrok paid plans"
echo ""

# Start ngrok
echo -e "${GREEN}🚀 Starting ngrok tunnel to http://localhost:5000${NC}"
echo ""
echo -e "${YELLOW}📋 Instructions:${NC}"
echo "1. Share the ngrok URL with workshop attendees"
echo "2. They can vote from their laptops!"
echo "3. Watch the votes increase in real-time"
echo "4. Press Ctrl+C to stop ngrok when done"
echo ""

ngrok http 5000 