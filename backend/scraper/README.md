# Smart Port Innovation - Graph 1: Scraping Engine

## Overview
Autonomous data collection system that scrapes patents, RSS feeds, tech news, and academic papers every 5 hours. Outputs standardized signals to Graph 2 for AI processing.

## Architecture
- **Node 1:** Orchestrator (decides when to scrape)
- **Node 2:** Scraping Tools (4 parallel scrapers)
- **Node 3:** Quality Filter (basic validation)
- **Node 4:** Formatter (standardize to exact schema)
- **Node 5:** Handoff (publish to RabbitMQ)

## Quick Start
```bash
# Clone repository
git clone <repo-url>
cd graph-1-scraping

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Run manually (for testing)
python scripts/manual_trigger.py

# Start scheduler
celery -A scheduler.celery_app worker --loglevel=info
celery -A scheduler.celery_app beat --loglevel=info
```

## Output Schema
Each signal sent to Graph 2:
```json
{
  "id": "uuid",
  "url": "https://...",
  "source": "Source Name",
  "title": "Title",
  "text": "FULL CONTENT",
  "scraping_date": "2026-02-06T14:30:00Z",
  "is_processed": false
}
```

## Configuration
- `config/sources.yaml`: Source APIs and feeds
- `config/keywords.yaml`: Search keywords by domain
- `config/schedule.yaml`: Scraping schedule (default: every 5 hours)

## Testing
```bash
pytest tests/
```

## Monitoring
- RabbitMQ Management: http://localhost:15672
- MinIO Console: http://localhost:9001