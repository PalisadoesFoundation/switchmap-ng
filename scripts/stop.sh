#!/bin/bash
# ==============================================================================
# Switchmap-NG Stop Script
# ==============================================================================
# Stops all Switchmap-NG services
# Usage: scripts/stop.sh
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/common.sh"

cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}Stopping Switchmap-NG Services...${NC}"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    print_warning "Virtual environment not found"
fi

# Stop server
print_info "Stopping server daemon..."
if python3 bin/systemd/switchmap_server --stop 2>/dev/null; then
    print_success "Server stopped"
else
    print_warning "Server was not running or failed to stop"
fi

# Stop poller
print_info "Stopping poller daemon..."
if python3 bin/systemd/switchmap_poller --stop 2>/dev/null; then
    print_success "Poller stopped"
else
    print_warning "Poller was not running or failed to stop"
fi

# Stop ingester
print_info "Stopping ingester daemon..."
if python3 bin/systemd/switchmap_ingester --stop 2>/dev/null; then
    print_success "Ingester stopped"
else
    print_warning "Ingester was not running or failed to stop"
fi

# Stop frontend
if [ -f var/daemon/pid/frontend.pid ]; then
    FRONTEND_PID=$(cat var/daemon/pid/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_info "Stopping frontend..."
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 1
        
        # Force kill if still running
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        fi
        
        print_success "Frontend stopped"
    fi
    rm -f var/daemon/pid/frontend.pid
fi

# Also kill any remaining npm processes
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true

# Clean up PID files
rm -f var/daemon/pid/*.pid 2>/dev/null || true

echo ""
print_success "All services stopped!"
echo ""

