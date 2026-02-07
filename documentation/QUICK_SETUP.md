# ⚡ Quick Setup Guide

Get MicroHack 3.0 running in under 5 minutes.

## 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- (Windows Only) PowerShell or CMD.

## 2. Launch (One Command)
Open a terminal in the project root and run:
```powershell
docker compose up --build
```
*Wait ~2-3 minutes for the first build and database initialization.*

## 3. Verify Success
Check these links to confirm everything is online:
- **Main Dashboard**: [http://localhost](http://localhost) (Should see market signals)
- **API Status**: [http://localhost:8000/health](http://localhost:8000/health) (Should return `{"status": "ok"}`)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive Swagger UI)

## 4. Troubleshooting
- **Port Conflict**: Ensure ports **80, 8000, 5432, 6379, 5672, and 9000** are free.
- **Empty Dashboard**: The scraper starts automatically but takes ~60 seconds to populate the first signals. Refresh after 1 minute.
- **Old Containers**: If you get a "name conflict" error, run:
  `docker compose down` then try again.
