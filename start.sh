#!/bin/bash
# ==============================================================================
# Switchmap-NG Start Script
# ==============================================================================
# Starts all Switchmap-NG services
# Usage: ./start.sh [OPTIONS]
# Options:
#   --skip-frontend   Skip starting frontend
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKIP_FRONTEND=false

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}▶${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-frontend) SKIP_FRONTEND=true; shift ;;
        *) print_error "Unknown option: $1"; exit 1 ;;
    esac
done

cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}Starting Switchmap-NG Services...${NC}"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    print_error "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Clean up old PID files
rm -f var/daemon/pid/*.pid 2>/dev/null || true

# Start server
print_info "Starting server daemon..."
if python3 bin/systemd/switchmap_server --start; then
    sleep 3
    if python3 bin/systemd/switchmap_server --status > /dev/null 2>&1; then
        print_success "Server started (port 7010)"
    else
        print_warning "Server may not have started correctly"
    fi
else
    print_error "Failed to start server"
    exit 1
fi

# Start poller
print_info "Starting poller daemon..."
if python3 bin/systemd/switchmap_poller --start; then
    sleep 2
    if python3 bin/systemd/switchmap_poller --status > /dev/null 2>&1; then
        print_success "Poller started"
    else
        print_warning "Poller may not have started correctly"
    fi
else
    print_error "Failed to start poller"
fi

# Start ingester
print_info "Starting ingester daemon..."
if python3 bin/systemd/switchmap_ingester --start; then
    sleep 2
    if python3 bin/systemd/switchmap_ingester --status > /dev/null 2>&1; then
        print_success "Ingester started"
    else
        print_warning "Ingester may not have started correctly"
    fi
else
    print_error "Failed to start ingester"
fi

# Start frontend
if ! $SKIP_FRONTEND; then
    print_info "Starting frontend..."
    cd frontend
    
    # Kill existing frontend process if any
    if [ -f ../var/daemon/pid/frontend.pid ]; then
        OLD_PID=$(cat ../var/daemon/pid/frontend.pid)
        if ps -p $OLD_PID > /dev/null 2>&1; then
            kill $OLD_PID 2>/dev/null || true
        fi
    fi
    
    # Start new frontend
    npm run dev > ../var/log/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../var/daemon/pid/frontend.pid
    
    sleep 3
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_success "Frontend started (port 7011)"
    else
        print_warning "Frontend may not have started correctly"
    fi
    
    cd "$PROJECT_ROOT"
fi

echo ""
print_success "All services started!"
echo ""
echo -e "${BLUE}Access Points:${NC}"
echo -e "  Server:   ${GREEN}http://localhost:7010${NC}"
if ! $SKIP_FRONTEND; then
    echo -e "  Frontend: ${GREEN}http://localhost:7011${NC}"
fi
echo ""
echo -e "Run ${BLUE}./status.sh${NC} to check service status"
echo -e "Run ${BLUE}./logs.sh${NC} to view logs"
echo ""

