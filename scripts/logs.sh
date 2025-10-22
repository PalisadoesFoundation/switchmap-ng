#!/bin/bash
# ==============================================================================
# Switchmap-NG Logs Script
# ==============================================================================
# Tails logs from all Switchmap-NG services
# Usage: ./logs.sh [SERVICE]
#   SERVICE: server, poller, ingester, frontend, all (default)
# ==============================================================================


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVICE="${1:-all}"

source "$SCRIPT_DIR/common.sh"

cd "$PROJECT_ROOT" || exit 1;

case $SERVICE in
    server)
        echo -e "${CYAN}=== Server Logs ===${NC}"
        tail -f var/log/switchmap-server.log
        ;;
    poller)
        echo -e "${CYAN}=== Poller Logs ===${NC}"
        tail -f var/log/switchmap.log | grep -i --line-buffered "poll"
        ;;
    ingester)
        echo -e "${CYAN}=== Ingester Logs ===${NC}"
        tail -f var/log/switchmap.log | grep -i --line-buffered "ingest"
        ;;
    frontend)
        echo -e "${CYAN}=== Frontend Logs ===${NC}"
        if [ -f var/log/frontend.log ]; then
            tail -f var/log/frontend.log
        else
            echo "Frontend log not found"
            exit 1
        fi
        ;;
    all)
        echo -e "${CYAN}=== All Logs (Combined) ===${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        
        # Use tail to follow multiple files
        if [ -f var/log/frontend.log ]; then
            tail -f var/log/switchmap.log var/log/switchmap-server.log var/log/frontend.log 2>/dev/null
        else
            tail -f var/log/switchmap.log var/log/switchmap-server.log 2>/dev/null
        fi
        ;;
    *)
        echo -e "${BLUE}Usage: ./logs.sh [SERVICE]${NC}"
        echo ""
        echo "Available services:"
        echo "  server    - Server daemon logs"
        echo "  poller    - Poller daemon logs"
        echo "  ingester  - Ingester daemon logs"
        echo "  frontend  - Frontend logs"
        echo "  all       - All logs combined (default)"
        echo ""
        exit 1
        ;;
esac

