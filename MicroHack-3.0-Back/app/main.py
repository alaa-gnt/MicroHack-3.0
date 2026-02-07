from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import signals, pipeline, alerts, analytics, knowledge_base, auth, opportunities, feasibility, alert_rules

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
