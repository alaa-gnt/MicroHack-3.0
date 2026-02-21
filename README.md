# 🚀 MicroHack 3.0: Intelligence Engine & Strategic Surveillance

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-orange?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

Welcome to **MicroHack 3.0**, a professional-grade competitive intelligence platform designed to decode market signals, identify strategic gaps, and provide actionable insights for innovation strategies.

---

## 🏗️ System Architecture

Our platform is a multi-agent ecosystem designed for high-performance data processing:

1.  **Scraping Engine**: Automatically harvests data from Patents, RSS feeds, Tech News, and Academic sources.
2.  **Multi-Agent Tier 1 (Analyst)**: Uses AI (LangGraph + Gemini) to clean, categorize, and score incoming signals for Impact and Urgency.
3.  **Multi-Agent Tier 2 (Deep Dive)**: Performs feasibility studies on high-scoring opportunities, generating tech stacks and strategic recommendations.
4.  **Dashboard**: A React-based command center for real-time strategic surveillance.

### 🔄 Agent Workflow
```mermaid
graph TD
    A[Scraper] -->|Raw Signals| B(Tier-1 Agent: Analysis)
    B -->|Enriched Data| C{Scoring > 0.8?}
    C -- Yes --> D(Tier-2 Agent: Deep Dive)
    C -- No --> E[Storage Only]
    D -->|Feasibility Report| F[Venture Blueprint]
    F --> G[Dashboard]
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic.
- **Frontend**: React, Vite, CSS Modules.
- **Agents**: LangGraph, LangChain, Google Gemini Pro.
- **Infrastructure**: Docker, Redis, RabbitMQ, PostgreSQL, MinIO.

---

## ⚡ Setup & Execution

### 1. Prerequisites
- Docker & Docker Compose installed.

### 2. Build and Run
To build the images and start the entire ecosystem in one go, run:
```bash
docker compose up --build
```

---

## 🌐 Accessing the Platform

Once the containers are running:

- **Dashboard (Frontend)**: [http://localhost](http://localhost)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 📁 Repository Structure

```text
.
├── backend/            # FastAPI API & Multi-Agent Logic
│   ├── agents/         # LangGraph Tier-1 & Tier-2 scripts
│   ├── app/            # Main FastAPI application
│   ├── scraper/        # Scraper Graph logic
│   └── scripts/        # Database & Utility scripts
├── frontend/           # React + Vite Dashboard
├── documentation/      # Detailed ARCHITECTURE & HACKATHON info
└── docker-compose.yml  # System Orchestration
```

---

## 🏆 Development
Developed for the **MicroHack 3.0 Hackathon**. This project demonstrates the power of multi-agent systems in corporate scouting and competitive intelligence.

---

## 🤝 Connect
Let's connect on **[LinkedIn](https://www.linkedin.com/in/YOUR_PROFILE_HERE/)**!
