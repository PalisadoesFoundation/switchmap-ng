#!/bin/bash
# ==============================================================================
# Switchmap-NG Cleanup Script
# ==============================================================================
# Removes all generated files and resets to clean state
# Usage: scripts/cleanup.sh [OPTIONS]
# Options:
#   --keep-mysql      Keep MySQL data
#   --keep-venv       Keep Python virtual environment
#   --full            Complete cleanup (removes everything)
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KEEP_MYSQL=false
KEEP_VENV=false
FULL_CLEANUP=false

source "$SCRIPT_DIR/common.sh"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-mysql) KEEP_MYSQL=true; shift ;;
        --keep-venv) KEEP_VENV=true; shift ;;
        --full) FULL_CLEANUP=true; shift ;;
        *) print_error "Unknown option: $1"; exit 1 ;;
    esac
done

cd "$PROJECT_ROOT" || exit 1

echo ""
echo -e "${RED}|              Switchmap-NG Cleanup                |${NC}"
echo ""

print_warning "This will remove generated files and stop all services"
echo ""

if $FULL_CLEANUP; then
    print_warning "FULL CLEANUP MODE: This will remove EVERYTHING including MySQL data!"
fi

read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Cleanup cancelled"
    exit 0
fi

echo ""

# Stop all services
print_info "Stopping all services..."
"$SCRIPT_DIR/stop.sh" 2>/dev/null || true

# Remove var directory (logs, cache, pid files)
print_info "Removing var directory..."
if $FULL_CLEANUP || ! $KEEP_MYSQL; then
    rm -rf var/*
    mkdir -p var/log var/cache var/snmp var/daemon/pid var/daemon/lock
    chmod -R 755 var
    chmod -R 700 var/daemon/pid
    print_success "var directory cleaned"
else
    rm -rf var/log/* var/cache/* var/daemon/pid/* var/daemon/lock/*
    print_success "var directory cleaned (kept structure)"
fi

# Remove Python virtual environment
if $FULL_CLEANUP || ! $KEEP_VENV; then
    if [ -d "venv" ]; then
        print_info "Removing Python virtual environment..."
        rm -rf venv
        print_success "Virtual environment removed"
    fi
fi

# Remove config file
if $FULL_CLEANUP; then
    if [ -f "etc/config.yaml" ]; then
        print_info "Removing configuration file..."
        rm -f etc/config.yaml
        print_success "Configuration removed"
    fi
fi

# Remove frontend node_modules (if full cleanup)
if $FULL_CLEANUP; then
    if [ -d "frontend/node_modules" ]; then
        print_info "Removing frontend node_modules..."
        rm -rf frontend/node_modules
        print_success "Frontend dependencies removed"
    fi
fi

# Remove MySQL Docker container
if $FULL_CLEANUP || ! $KEEP_MYSQL; then
    if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^switchmap-mysql$'; then
        print_info "Removing MySQL Docker container..."
        docker stop switchmap-mysql 2>/dev/null || true
        docker rm switchmap-mysql 2>/dev/null || true
        print_success "MySQL container removed"
    fi
fi

# Remove MySQL data volume (if full cleanup)
if $FULL_CLEANUP; then
    VOLUMES=$(docker volume ls --format '{{.Name}}' 2>/dev/null | grep -E '^switchmap(-|$)' || true)
    if [ -n "$VOLUMES" ]; then
        print_info "Removing MySQL data volumes..."
        echo "$VOLUMES" | xargs -r docker volume rm 2>/dev/null || true
        print_success "MySQL data volumes removed"
    fi
fi

# Remove Python cache
print_info "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
print_success "Python cache cleaned"

echo ""
print_success "Cleanup complete!"
echo ""

if $FULL_CLEANUP; then
    print_info "To setup again, run: scripts/setup.sh --docker-mysql"
else
    print_info "Removed temporary files. Run scripts/setup.sh to reinitialize."
fi

echo ""

