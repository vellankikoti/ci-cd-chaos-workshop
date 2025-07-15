#!/bin/bash

# 🚀 Expose Voting App via Cloudflare Tunnel
# ===========================================
# This script exposes the local voting app via Cloudflare Tunnel for public access

set -e

# Color codes for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Exposing Voting App via Cloudflare Tunnel...${NC}"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}⚠️  cloudflared not found. Installing...${NC}"
    echo "Please install cloudflared first:"
    echo "  brew install cloudflared"
    echo ""
    echo "Or download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
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
echo -e "${BLUE}🌐 Starting Cloudflare Tunnel...${NC}"
echo "This will create a public URL that anyone can access!"
echo ""
echo -e "${YELLOW}📝 Note: Cloudflare Tunnel features:${NC}"
echo "  • Free and unlimited tunnels"
echo "  • No connection limits"
echo "  • Automatic HTTPS"
echo "  • Global CDN"
echo ""

# Start cloudflared
echo -e "${GREEN}🚀 Starting Cloudflare Tunnel to http://localhost:5000${NC}"
echo ""
echo -e "${YELLOW}📋 Instructions:${NC}"
echo "1. Share the Cloudflare URL with workshop attendees"
echo "2. They can vote from their laptops!"
echo "3. Watch the votes increase in real-time"
echo "4. Press Ctrl+C to stop the tunnel when done"
echo ""

cloudflared tunnel --url http://localhost:5000 