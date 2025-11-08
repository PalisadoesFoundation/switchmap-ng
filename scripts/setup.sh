#!/bin/bash
# ==============================================================================
# Switchmap-NG Automated Setup Script
# ==============================================================================
# This script automates the entire setup process for Switchmap-NG
# Usage: scripts/setup.sh [OPTIONS]
# Options:
#   --docker-mysql    Use Docker for MySQL (recommended)
#   --local-mysql     Use local MySQL installation
#   --help           Show this help message
# ==============================================================================

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
USE_DOCKER_MYSQL=false
USE_LOCAL_MYSQL=false

# MySQL Configuration
MYSQL_ROOT_PASSWORD="switchmap_root_2024"
MYSQL_DATABASE="switchmap"
MYSQL_USER="switchmap"
MYSQL_PASSWORD="switchmap_password"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"

# ==============================================================================
# Helper Functions
# ==============================================================================

print_header() {
    echo -e "${CYAN}"
    echo "|           Switchmap-NG Automated Setup v1.0             |"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} ${GREEN}▶${NC} $1"
}

source "$SCRIPT_DIR/common.sh"

# ==============================================================================
# Prerequisite Checks
# ==============================================================================

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check Python 3.9+
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        missing_deps+=("python3")
        print_error "Python 3 not found"
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        missing_deps+=("pip3")
        print_error "pip3 not found"
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        missing_deps+=("node")
        print_error "Node.js not found"
    fi
        
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm found: $NPM_VERSION"
    else
        missing_deps+=("npm")
        print_error "npm not found"
    fi
    
    # Check Docker if needed
    if $USE_DOCKER_MYSQL; then
        if command -v docker &> /dev/null; then
            print_success "Docker found"
        else
            missing_deps+=("docker")
            print_error "Docker not found (required for --docker-mysql)"
        fi
    fi
    
    # Check MySQL client
    if command -v mysql &> /dev/null; then
        print_success "MySQL client found"
    else
        print_warning "MySQL client not found (optional)"
    fi
    
    # Exit if missing critical dependencies
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install the missing dependencies and try again."
        echo ""
        echo "macOS:"
        echo "  brew install python3 node mysql-client"
        echo "  (Docker Desktop from https://www.docker.com/products/docker-desktop)"
        echo ""
        echo "Ubuntu/Debian:"
        echo "  sudo apt-get install python3 python3-pip nodejs npm mysql-client docker.io"
        echo ""
        exit 1
    fi
    
    echo ""
}

# ==============================================================================
# MySQL Setup
# ==============================================================================

setup_mysql_docker() {
    print_step "Setting up MySQL with Docker..."
    
    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q '^switchmap-mysql$'; then
        print_info "MySQL container already exists"
        
        # Check if running
        if docker ps --format '{{.Names}}' | grep -q '^switchmap-mysql$'; then
            print_success "MySQL container is already running"
        else
            print_info "Starting existing MySQL container..."
            docker start switchmap-mysql
            sleep 5
            print_success "MySQL container started"
        fi
    else
        print_info "Creating new MySQL container..."
        docker run -d \
            --name switchmap-mysql \
            -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
            -e MYSQL_DATABASE="$MYSQL_DATABASE" \
            -e MYSQL_USER="$MYSQL_USER" \
            -e MYSQL_PASSWORD="$MYSQL_PASSWORD" \
            -p 3306:3306 \
            mysql:8.0 \
            --default-authentication-plugin=mysql_native_password
        
        print_info "Waiting for MySQL to be ready..."
        sleep 15
        
        # Wait for MySQL to be healthy
        for i in {1..30}; do
            if docker exec switchmap-mysql mysqladmin ping -h localhost -u root -p"$MYSQL_ROOT_PASSWORD" --silent 2>/dev/null; then
                print_success "MySQL is ready!"
                break
            fi
            echo -n "."
            sleep 2
        done
        echo ""
    fi
    
    # Verify database and user
    print_info "Verifying database setup..."
    docker exec switchmap-mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "
        CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
        CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
        GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';
        FLUSH PRIVILEGES;
    " 2>/dev/null
    
    print_success "MySQL setup complete (Docker)"
    echo ""
}

setup_mysql_local() {
    print_step "Setting up local MySQL database..."
    
    print_info "Please enter your MySQL root password when prompted."
    
    mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
CREATE USER IF NOT EXISTS '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
    
    if [ $? -eq 0 ]; then
        print_success "MySQL database and user created"
    else
        print_error "Failed to setup MySQL database"
        exit 1
    fi
    
    echo ""
}

# ==============================================================================
# Python Environment Setup
# ==============================================================================

setup_python_env() {
    print_step "Setting up Python virtual environment..."
    
    cd "$PROJECT_ROOT"
    
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip --quiet
    
    # Install requirements
    print_info "Installing Python dependencies (this may take a few minutes)..."
    pip install -r requirements.txt --quiet
    
    print_success "Python environment ready"
    echo ""
}

# ==============================================================================
# Configuration Setup
# ==============================================================================

setup_config() {
    print_step "Setting up configuration..."
    
    cd "$PROJECT_ROOT"
    
    # Create etc directory if it doesn't exist
    mkdir -p etc
    
    # Get current username
    CURRENT_USER=$(whoami)
    
    # Copy config if it doesn't exist
    if [ ! -f "etc/config.yaml" ]; then
        print_info "Copying configuration template..."
        cp examples/etc/config.yaml etc/config.yaml
        
        print_success "Configuration file created: etc/config.yaml"
    else
        print_success "Configuration file already exists"
    fi
    
    # Always update configuration (whether new or existing)
    print_info "Updating configuration..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/db_host:.*/db_host: $MYSQL_HOST/" etc/config.yaml
        sed -i '' "s/db_name:.*/db_name: $MYSQL_DATABASE/" etc/config.yaml
        sed -i '' "s/db_user:.*/db_user: $MYSQL_USER/" etc/config.yaml
        sed -i '' "s/db_pass:.*/db_pass: $MYSQL_PASSWORD/" etc/config.yaml
        # Update usernames (server and poller) - replace any existing username
        sed -i '' "s/username:.*/username: $CURRENT_USER/" etc/config.yaml
        # Update server addresses for local setup (not Docker)
        sed -i '' "s/server_address: switchmap-server/server_address: localhost/g" etc/config.yaml
        sed -i '' "s/server_address: switchmap-mysql/server_address: localhost/g" etc/config.yaml
    else
        # Linux
        sed -i "s/db_host:.*/db_host: $MYSQL_HOST/" etc/config.yaml
        sed -i "s/db_name:.*/db_name: $MYSQL_DATABASE/" etc/config.yaml
        sed -i "s/db_user:.*/db_user: $MYSQL_USER/" etc/config.yaml
        sed -i "s/db_pass:.*/db_pass: $MYSQL_PASSWORD/" etc/config.yaml

        # Update usernames (server and poller) - replace any existing username
        # Using current system username
        sed -i "s/username:.*/username: $CURRENT_USER/" etc/config.yaml

        # Update server addresses for local setup (not Docker)
        sed -i "s/server_address: switchmap-server/server_address: localhost/g" etc/config.yaml
        sed -i "s/server_address: switchmap-mysql/server_address: localhost/g" etc/config.yaml
    fi
    
    print_success "Configuration updated"
    print_info "Username set to: $CURRENT_USER"
    print_info "Database credentials configured"
    
    # Create var directory structure
    print_info "Creating var directory structure..."
    mkdir -p var/log var/cache var/snmp var/daemon/pid var/daemon/lock
    chmod -R 755 var
    chmod -R 700 var/daemon/pid
    
    print_success "Directory structure created"
    echo ""
}

# ==============================================================================
# Database Initialization
# ==============================================================================

init_database() {
    print_step "Initializing database..."
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Create tables
    print_info "Creating database tables..."
    python3 bin/tools/create_db_tables.py
    
    if [ $? -eq 0 ]; then
        print_success "Database tables created"
    else
        print_error "Failed to create database tables"
        exit 1
    fi
    
    # Ingest OUI data
    print_info "Ingesting OUI data (this may take a minute)..."
    python3 bin/tools/process_oiu_file.py --new_installation
    
    if [ $? -eq 0 ]; then
        print_success "OUI data ingested"
    else
        print_warning "OUI data ingestion had issues (non-critical)"
    fi
    
    echo ""
}

# ==============================================================================
# Start Daemons
# ==============================================================================

start_daemons() {
    print_step "Starting Switchmap daemons..."
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Clean up old PID files
    rm -f var/daemon/pid/*.pid 2>/dev/null || true

    print_step "Setting up frontend..."
    
    cd "$PROJECT_ROOT/frontend"
    
    # Install dependencies
    print_info "Installing frontend dependencies (this may take a few minutes)..."
    npm install --silent
    
    print_success "Frontend dependencies installed"
    
    # Start dev server in background
    print_info "Starting frontend dev server..."
    npm run dev > ../var/log/frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # Save PID
    echo $FRONTEND_PID > ../var/daemon/pid/frontend.pid
    
    # Wait for frontend to be ready
    print_info "Waiting for frontend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready at http://localhost:3000"
            break
        fi
        sleep 1
    done

    if ! $FRONTEND_READY; then
    print_warning "Frontend may not have started correctly"
    fi
    
    cd "$PROJECT_ROOT"
    echo ""
    
    # Start server
    print_info "Starting server daemon..."
    python3 bin/systemd/switchmap_server --start
    sleep 3
    
    # Check server status
    if python3 bin/systemd/switchmap_server --status > /dev/null 2>&1; then
        print_success "Server daemon started (GraphQL + HTTP API on port 7010)"
    else
        print_error "Server daemon failed to start"
        exit 1
    fi
    
    # Start poller
    print_info "Starting poller daemon..."
    python3 bin/systemd/switchmap_poller --start
    sleep 2
    
    if python3 bin/systemd/switchmap_poller --status > /dev/null 2>&1; then
        print_success "Poller daemon started"
    else
        print_warning "Poller daemon may not have started correctly"
    fi
    
    # Start ingester
    print_info "Starting ingester daemon..."
    python3 bin/systemd/switchmap_ingester --start
    sleep 2
    
    if python3 bin/systemd/switchmap_ingester --status > /dev/null 2>&1; then
        print_success "Ingester daemon started"
    else
        print_warning "Ingester daemon may not have started correctly"
    fi
    
    echo ""

}

# ==============================================================================
# Main Setup
# ==============================================================================

show_usage() {
    cat << EOF
Usage: scripts/setup.sh [OPTIONS]

Automated setup script for Switchmap-NG

Options:
    --docker-mysql    Use Docker for MySQL (recommended)
    --local-mysql     Use local MySQL installation
    --help           Show this help message

Examples:
    scripts/setup.sh --docker-mysql           # Use Docker MySQL (recommended)
    scripts/setup.sh --local-mysql            # Use local MySQL

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --docker-mysql)
                USE_DOCKER_MYSQL=true
                shift
                ;;
            --local-mysql)
                USE_LOCAL_MYSQL=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate arguments
    if ! $USE_DOCKER_MYSQL && ! $USE_LOCAL_MYSQL; then
        print_error "Please specify either --docker-mysql or --local-mysql"
        echo ""
        show_usage
        exit 1
    fi
    
    if $USE_DOCKER_MYSQL && $USE_LOCAL_MYSQL; then
        print_error "Cannot use both --docker-mysql and --local-mysql"
        echo ""
        show_usage
        exit 1
    fi
}

show_completion_message() {
    echo ""
    echo -e "${GREEN}|<---     ✓ Setup Complete!      --->|${NC}"
    echo ""
    echo -e "${CYAN}Services Running:${NC}"
    echo -e "  ${GREEN}▶${NC} Server:   http://localhost:7010 (API + GraphQL)"
    echo -e "  ${GREEN}▶${NC} Frontend: http://localhost:3000 (Web UI)"
    echo ""
    echo -e "${CYAN}Useful Commands:${NC}"
    echo -e "  ${BLUE}scripts/start.sh${NC}    - Start all services"
    echo -e "  ${BLUE}scripts/stop.sh${NC}     - Stop all services"
    echo -e "  ${BLUE}scripts/status.sh${NC}   - Check service status"
    echo -e "  ${BLUE}scripts/logs.sh${NC}     - View logs"
    echo -e "  ${BLUE}scripts/restart.sh${NC}  - Restart all services"
    echo ""
    echo -e "${CYAN}Log Files:${NC}"
    echo -e "  ${BLUE}var/log/switchmap.log${NC}        - Main application log"
    echo -e "  ${BLUE}var/log/switchmap-server.log${NC} - Server daemon log"
    echo -e "  ${BLUE}var/log/frontend.log${NC}         - Frontend log"

    echo ""
    echo -e "${GREEN} Open your browser to http://localhost:3000 to get started!${NC}"
    echo ""
        
    # Try to open browser
    if command -v open &> /dev/null; then
        # macOS
        sleep 2
        open http://localhost:3000
    elif command -v xdg-open &> /dev/null; then
        # Linux
        sleep 2
        xdg-open http://localhost:3000
    fi
}

main() {
    print_header
    parse_args "$@"
    
    check_prerequisites
    
    # Setup MySQL
    if $USE_DOCKER_MYSQL; then
        setup_mysql_docker
    else
        setup_mysql_local
    fi
    
    setup_python_env
    setup_config
    init_database
    start_daemons
    show_completion_message
}

# Run main
main "$@"

