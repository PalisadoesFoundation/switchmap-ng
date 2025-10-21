#!/bin/bash
# ==============================================================================
# Switchmap-NG Restart Script
# ==============================================================================
# Restarts all Switchmap-NG services
# Usage: ./restart.sh
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}Restarting Switchmap-NG Services...${NC}"
echo ""

# Stop all services
./stop.sh

# Wait a moment
echo ""
echo -e "${BLUE}Waiting 3 seconds before restart...${NC}"
sleep 3

# Start all services
./start.sh

echo ""
echo -e "${GREEN}Restart complete!${NC}"
echo ""

