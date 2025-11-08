# Switchmap-NG Quick Reference Card

## One-Command Setup

```bash
scripts/setup.sh --docker-mysql
```

## Common Commands

| Command | Description |
|---------|-------------|
| `scripts/setup.sh --docker-mysql` | Initial setup with Docker MySQL |
| `scripts/setup.sh --local-mysql` | Initial setup with local MySQL |
| `scripts/start.sh` | Start all services |
| `scripts/stop.sh` | Stop all services |
| `scripts/restart.sh` | Restart all services |
| `scripts/status.sh` | Check service status |
| `scripts/logs.sh` | View all logs |
| `scripts/logs.sh server` | View server logs only |
| `scripts/cleanup.sh` | Clean temporary files |
| `scripts/cleanup.sh --full` | Complete cleanup |

## Access URLs

- **Frontend:** http://localhost:3000
- **GraphQL:** http://localhost:7010/switchmap/graphql
- **REST API:** http://localhost:7010/switchmap/api

## Important Files

- **Config:** `etc/config.yaml`
- **Main Log:** `var/log/switchmap.log`
- **Server Log:** `var/log/switchmap-server.log`
- **Frontend Log:** `var/log/frontend.log`

## Quick Troubleshooting

```bash
# Check what's running
scripts/status.sh

# View live logs
scripts/logs.sh

# Restart everything
scripts/restart.sh

# Complete reset
scripts/stop.sh
scripts/cleanup.sh --full
scripts/setup.sh --docker-mysql
```

## Tips

- First setup takes 2-3 minutes
- Logs are your friend: `scripts/logs.sh`
- Stop services before shutdown: `scripts/stop.sh`
- Check status often: `scripts/status.sh`

## Help

Full documentation: `SETUP_GUIDE.md`

