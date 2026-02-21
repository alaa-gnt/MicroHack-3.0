from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import signals, pipeline, alerts, analytics, knowledge_base, auth, opportunities, feasibility, alert_rules, blueprints

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(signals.router, prefix=f"{settings.API_V1_STR}/signals", tags=["Signals"])
app.include_router(pipeline.router, prefix=f"{settings.API_V1_STR}/pipeline", tags=["Pipeline"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["Alerts"])
app.include_router(alert_rules.router, prefix=f"{settings.API_V1_STR}/alert-rules", tags=["Alert Rules"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
app.include_router(knowledge_base.router, prefix=f"{settings.API_V1_STR}/kb", tags=["Knowledge Base"])
app.include_router(opportunities.router, prefix=f"{settings.API_V1_STR}/opportunities", tags=["Opportunities"])
app.include_router(feasibility.router, prefix=f"{settings.API_V1_STR}/feasibility-studies", tags=["Feasibility Studies"])
app.include_router(blueprints.router, prefix=f"{settings.API_V1_STR}/blueprints", tags=["Venture Blueprints"])

# Startup Event
import threading
from app.database.postgres import SessionLocal
from app.services.pipeline_service import PipelineService

def run_initial_scrape():
    """
    Runs the scraper in a background thread on startup.
    """
    print("🚀 [STARTUP] Triggering initial scraping pipeline...")
    db = SessionLocal()
    try:
        # Run with default sources/keywords
        PipelineService.run_scraping_pipeline(db)
        print("✅ [STARTUP] Initial scraping pipeline completed.")
    except Exception as e:
        print(f"❌ [STARTUP] Initial scraping failed: {e}")
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    # Run in a separate thread so we don't block the server startup
    threading.Thread(target=run_initial_scrape, daemon=True).start()
