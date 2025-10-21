# Switchmap-NG Automated Setup Guide

## Quick Start

Get Switchmap-NG running with one command:

```bash
scripts/setup.sh --docker-mysql
```

That's it! The script will:
- Check prerequisites
- Setup MySQL (Docker container)
- Create Python virtual environment
- Install all dependencies
- Create database tables
- Ingest OUI data
- Start all daemons
- Launch frontend
- Open browser to http://localhost:3000

---

## Prerequisites

### Required:
- **Python 3.9+** - Backend runtime
- **Node.js 16+** - Frontend runtime
- **npm** - Package manager

### Optional (for Docker MySQL):
- **Docker** - For containerized MySQL

### Installation:

**macOS:**
```bash
brew install python3 node
# Install Docker Desktop from https://www.docker.com/products/docker-desktop
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv nodejs npm
# For Docker: sudo apt-get install docker.io
```

---

## Detailed Setup

### Option 1: Docker MySQL (Recommended)

**Best for:** Development, testing, first-time users

```bash
scripts/setup.sh --docker-mysql
```

**Advantages:**
- No MySQL installation needed
- Isolated database
- Easy cleanup
- Consistent across platforms

### Option 2: Local MySQL

**Best for:** Production, existing MySQL setup

```bash
scripts/setup.sh --local-mysql
```

**Requirements:**
- MySQL 8.0+ installed and running
- Root access to create database and user

**Note:** You'll be prompted for MySQL root password during setup.


---

## Management Commands

### Start Services

```bash
scripts/start.sh
```

Starts all daemons and frontend.

### Stop Services

```bash
scripts/stop.sh
```

Gracefully stops all running services.

### Check Status

```bash
scripts/status.sh
```

Shows detailed status of all services:
- Server daemon (API + GraphQL)
- Poller daemon
- Ingester daemon
- Frontend
- MySQL database
- Port usage
- Recent activity

### View Logs

```bash
# All logs combined
scripts/logs.sh

# Specific service logs
scripts/logs.sh server
scripts/logs.sh poller
scripts/logs.sh ingester
scripts/logs.sh frontend
```

Press `Ctrl+C` to stop tailing logs.

### Restart Services

```bash
scripts/restart.sh
```

Stops and starts all services with a 3-second delay.

### Cleanup

```bash
# Remove logs and temporary files
scripts/cleanup.sh

# Keep MySQL data
scripts/cleanup.sh --keep-mysql

# Keep Python venv
scripts/cleanup.sh --keep-venv

# Complete cleanup (remove everything)
scripts/cleanup.sh --full
```

---

## Configuration

### Main Configuration File

`etc/config.yaml` - Created automatically from `examples/etc/config.yaml`

**Key settings:**

```yaml
server:
  api_bind_port: 7010        # Server API port
  db_host: localhost         # MySQL host
  db_name: switchmap         # Database name
  db_user: switchmap         # Database user
  db_pass: switchmap_password # Database password
  ingest_interval: 90        # Ingestion interval (seconds)

dashboard:
  api_bind_port: 7011        # Frontend port

poller:
  polling_interval: 300      # Polling interval (seconds)
  zones:                     # Device zones
    - zone: ZONE1
      hostnames:
        - 192.168.1.1
```

### Database Configuration

**Docker MySQL (default):**
- Host: `localhost`
- Port: `3306`
- Database: `switchmap`
- User: `switchmap`
- Password: `switchmap_password`

**Local MySQL:**
- Configured during setup
- Credentials stored in `etc/config.yaml`



## Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:7011 | Web UI |
| **GraphQL** | http://localhost:7010/switchmap/graphql | GraphQL API |
| **REST API** | http://localhost:7010/switchmap/api | REST endpoints |

---

## Troubleshooting

### Port Already in Use

**Problem:** Port 7010 or 7011 already in use

**Solution:**
```bash
# Find process using port
lsof -i :7010
lsof -i :7011

# Kill process
kill <PID>

# Or change port in etc/config.yaml
```

### Services Won't Start

**Check prerequisites:**
```bash
python3 --version  # Should be 3.9+
node --version     # Should be 16+
```

**Check logs:**
```bash
scripts/logs.sh server
cat var/log/switchmap.log
```

**Restart services:**
```bash
scripts/stop.sh
scripts/start.sh
```

### MySQL Connection Failed

**Docker MySQL:**
```bash
# Check container is running
docker ps | grep switchmap-mysql

# Restart container
docker restart switchmap-mysql

# Check logs
docker logs switchmap-mysql
```

**Local MySQL:**
```bash
# Test connection
mysql -u switchmap -p switchmap

# Check MySQL is running
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS
```

### Frontend Not Loading

**Check if service is running:**
```bash
scripts/status.sh
```

**Check logs:**
```bash
scripts/logs.sh frontend
```

**Restart frontend:**
```bash
cd frontend
npm run dev
```

### Database Tables Missing

**Recreate tables:**
```bash
source venv/bin/activate
python3 bin/tools/create_db_tables.py
python3 bin/tools/process_oiu_file.py --new_installation
```

---

## Testing the Setup

### 1. Check All Services Running

```bash
scripts/status.sh
```

All services should show `● RUNNING`.

### 2. Test Server API

```bash
curl http://localhost:7010/health
# Should return: {"status":"UP"}
```

### 3. Test Frontend

Open browser to http://localhost:3000

### 4. Check Database

```bash
# Docker MySQL
docker exec -it switchmap-mysql mysql -u switchmap -p switchmap

# Local MySQL
mysql -u switchmap -p switchmap

# Then:
SHOW TABLES;
SELECT COUNT(*) FROM smap_oui; 
```

---

## Daily Workflow

### Starting Your Day

```bash
scripts/start.sh
```

### Checking Status

```bash
scripts/status.sh
```

### Viewing Logs

```bash
scripts/logs.sh
```

### Making Changes

Edit code → Services auto-reload (frontend) or restart daemons:

```bash
scripts/restart.sh
```

### Ending Your Day

```bash
scripts/stop.sh
```

---

## Advanced Usage

### Custom MySQL Port

Edit `etc/config.yaml`:
```yaml
server:
  db_host: localhost
  db_port: 3307  # Custom port
```

### Custom API Port

Edit `etc/config.yaml`:
```yaml
server:
  api_bind_port: 8080  # Custom port
```

### Running in Production

```bash
# Use local MySQL
scripts/setup.sh --local-mysql

# Configure production settings in etc/config.yaml
# Set proper credentials, intervals, etc.
```

### Development Mode

```bash
# Setup with Docker MySQL
scripts/setup.sh --docker-mysql

# Start without frontend (backend only)
scripts/start.sh --skip-frontend

# Run frontend manually with hot-reload
cd frontend
npm run dev
```

---

## Additional Resources

- **Main README:** `README.md`
- **Installation Guide:** `INSTALLATION.md`
- **Documentation:** `DOCUMENTATION.md`
- **Configuration Examples:** `examples/etc/config.yaml`
- **Testing Guide:** `docs/testing.md`

---

## Getting Help

1. Check logs: `scripts/logs.sh`
2. Check status: `scripts/status.sh`
3. Try cleanup and re-setup: `scripts/cleanup.sh --full && scripts/setup.sh --docker-mysql`
4. Check GitHub Issues
5. Contact maintainers

---

## Notes

- **First run takes 2-3 minutes** (installing dependencies)
- **Subsequent runs take ~10 seconds** (starting services)
- **Logs are in** `var/log/`
- **Configuration is in** `etc/config.yaml`
- **Stop services before system shutdown** for clean exit
