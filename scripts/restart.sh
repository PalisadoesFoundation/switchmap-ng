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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}Restarting Switchmap-NG Services...${NC}"
echo ""

# Stop all services
"$SCRIPT_DIR/stop.sh"

# Wait a moment
echo ""
echo -e "${BLUE}Waiting 3 seconds before restart...${NC}"
sleep 3

# Start all services
"$SCRIPT_DIR/start.sh"

echo ""
echo -e "${GREEN}Restart complete!${NC}"
echo ""

