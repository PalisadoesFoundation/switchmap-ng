#!/bin/bash
# ==============================================================================
# Switchmap-NG Status Script
# ==============================================================================
# Shows status of all Switchmap-NG services
# Usage: scripts/status.sh
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_running() { echo -e "  ${GREEN}● RUNNING${NC}   $1"; }
print_stopped() { echo -e "  ${RED}● STOPPED${NC}   $1"; }
print_header() { echo -e "${CYAN}$1${NC}"; }

# Load common print helpers
source "$SCRIPT_DIR/common.sh"

cd "$PROJECT_ROOT" || exit 1;

echo ""
print_header " |<---            Switchmap-NG Service Status              --->|"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}Virtual environment not found. Run scripts/setup.sh first.${NC}"
    exit 1
fi

# Check server
echo -e "${BLUE}Server Daemon:${NC}"
if python3 bin/systemd/switchmap_server --status 2>&1 | grep -q "running"; then
    print_running "Port 7010 (API + GraphQL)"
    
    # Check if port is actually responding
    if curl -s http://localhost:7010/health > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} API health check passed"
    fi
else
    print_stopped "Not running"
fi

# Check poller
echo ""
echo -e "${BLUE}Poller Daemon:${NC}"
if python3 bin/systemd/switchmap_poller --status 2>&1 | grep -q "running"; then
    print_running "Polling devices"
else
    print_stopped "Not running"
fi

# Check ingester
echo ""
echo -e "${BLUE}Ingester Daemon:${NC}"
if python3 bin/systemd/switchmap_ingester --status 2>&1 | grep -q "running"; then
    print_running "Ingesting data"
else
    print_stopped "Not running"
fi

# Check frontend
echo ""
echo -e "${BLUE}Frontend:${NC}"
if [ -f var/daemon/pid/frontend.pid ]; then
    FRONTEND_PID=$(cat var/daemon/pid/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_running "Port 3000 (Web UI)"
        
        # Check if port is actually responding
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo -e "    ${GREEN}✓${NC} Frontend health check passed"
        fi
    else
        print_stopped "Not running (stale PID file)"
    fi
else
    print_stopped "Not running"
fi

# Check MySQL
echo ""
echo -e "${BLUE}MySQL Database:${NC}"
# Try Docker MySQL first
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^switchmap-mysql$'; then
    print_running "Docker container (switchmap-mysql)"
    if docker exec switchmap-mysql mysqladmin ping -h localhost -u switchmap -pswitchmap_password --silent 2>/dev/null; then
        echo -e "    ${GREEN}✓${NC} Database connection OK"
    fi
# Try local MySQL
elif mysqladmin ping -h localhost -u switchmap -pswitchmap_password --silent 2>/dev/null; then
    print_running "Local MySQL server"
    echo -e "    ${GREEN}✓${NC} Database connection OK"
else
    print_stopped "Not accessible"
fi

# Show port usage
echo ""
echo -e "${CYAN}Port Usage:${NC}"
if command -v lsof &> /dev/null; then
    if lsof -i :7010 > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Port 7010 (Server) - IN USE"
    else
        echo -e "  ${YELLOW}○${NC} Port 7010 (Server) - FREE"
    fi
    
    if lsof -i :3000 > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Port 3000 (Frontend) - IN USE"
    else
        echo -e "  ${YELLOW}○${NC} Port 3000 (Frontend) - FREE"
    fi
    
    if lsof -i :3306 > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Port 3306 (MySQL) - IN USE"
    else
        echo -e "  ${YELLOW}○${NC} Port 3306 (MySQL) - FREE"
    fi
fi

# Show recent activity
echo ""
echo -e "${CYAN}Recent Activity:${NC}"
if [ -f var/log/switchmap.log ]; then
    echo -e "  Last 3 log entries:"
    tail -3 var/log/switchmap.log | while read line; do
        echo -e "    ${line:0:80}"
    done
fi

echo ""
echo -e "${BLUE}Quick Actions:${NC}"
echo -e "  ${GREEN}scripts/start.sh${NC}   - Start all services"
echo -e "  ${GREEN}scripts/stop.sh${NC}    - Stop all services"
echo -e "  ${GREEN}scripts/restart.sh${NC} - Restart all services"
echo -e "  ${GREEN}scripts/logs.sh${NC}    - View live logs"
echo ""

