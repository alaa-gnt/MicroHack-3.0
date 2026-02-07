# 🚀 MicroHack 3.0: Intelligence Engine & Strategic Surveillance

Welcome to **MicroHack 3.0**, a professional-grade competitive intelligence platform designed to decode market signals, identify strategic gaps, and provide actionable insights for innovation strategies.

## 🏗️ System Architecture

Our platform is a multi-agent ecosystem designed for high-performance data processing:

1.  **Scraping Engine**: Automatically harvests data from Patents, RSS feeds, Tech News, and Academic sources.
2.  **Multi-Agent Tier 1 (Analyst)**: Uses AI to clean, categorize, and score incoming signals for Impact and Urgency.
3.  **Multi-Agent Tier 2 (Deep Dive)**: Performs feasibility studies on high-scoring opportunities, generating tech stacks and recommendations.
4.  **Dashboard**: A React-based command center for strategic surveillance.

---

## 🛠️ Prerequisites

To run this platform, you only need:
- **Docker** & **Docker Compose**

---

## ⚡ Setup & Execution

### 1. Build and Run (Recommended)
To build the images and start the entire ecosystem in one go, run:
```powershell
docker compose up --build
```

### 2. Manual Build
If you only want to build the images without starting the containers:
```powershell
docker compose build
```

---

## 🌐 Accessing the Platform

Once the containers are running:

- **Dashboard (Frontend)**: [http://localhost](http://localhost)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧩 Services Overview

All services are orchestrated via Docker Compose:

| Service | Description | Port |
| :--- | :--- | :--- |
| `dashboard` | React Vite Frontend (Nginx Served) | 80 |
| `api` | FastAPI Backend | 8000 |
| `t1-agent` | Tier 1 analyst watcher (Redis-driven) | - |
| `t2-agent` | Tier 2 deep-dive watcher (Redis-driven) | - |
| `db` | PostgreSQL 15 Database | 5432 |
| `redis` | Event-driven message broker | 6379 |
| `minio` | S3-compatible raw data storage | 9000 |
| `rabbitmq` | Scraper handoff queue | 5672 |

---

## 📈 Innovation Workflow

1.  **Startup**: Scraper triggers automatically on backend launch.
2.  **Analysis**: Signals flow into `t1-agent` for instant scoring.
3.  **Feasibility**: High-scoring signals are sent to `t2-agent` for full business analysis.
4.  **Visualization**: Real-time results appear on the dashboard.

---

**Developed for the MicroHack 3.0 Hackathon.** 🏆
