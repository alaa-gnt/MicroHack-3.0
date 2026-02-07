from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.dependencies import get_db, get_current_user
from app.schemas.analytics import DashboardResponse, MarketTrendResponse
from app.services.analytics_service import AnalyticsService
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from sqlalchemy import func

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Returns the comprehensive dashboard dataset including real-time metrics.
    """
    from datetime import date
    from app.models.alert import Alert
    from app.models.poc import POC
    from app.models.project import Project

    today = date.today()
    
    trends = AnalyticsService.get_market_trends(db)
    tech_radar = AnalyticsService.get_tech_radar(db)
    entities = AnalyticsService.get_entities(db)
    funnel = AnalyticsService.get_funnel(db)
    benchmarks = AnalyticsService.get_benchmarks(db)
    
    # Real-time counts
    total_signals = db.query(func.count(Signal.id)).scalar() or 0
    total_opportunities = db.query(func.count(Opportunity.id)).scalar() or 0
    active_projects = db.query(func.count(Project.id)).scalar() or 0
    running_pocs = db.query(func.count(POC.id)).scalar() or 0
    alerts_today = db.query(func.count(Alert.id)).filter(func.date(Alert.created_at) == today).scalar() or 0

    # Breakdown of today's alerts
    alerts_critical = db.query(func.count(Alert.id)).filter(
        func.date(Alert.created_at) == today,
        Alert.severity.in_(['Critical', 'High'])
    ).scalar() or 0

    alerts_minor = db.query(func.count(Alert.id)).filter(
        func.date(Alert.created_at) == today,
        Alert.severity.in_(['Medium', 'Low'])
    ).scalar() or 0

    return {
        "status": "success",
        "trends": trends,
        "tech_radar": tech_radar,
        "entities": entities,
        "funnel": funnel,
        "benchmarks": benchmarks,
        "metrics": {
            "total_signals": total_signals,
            "total_opportunities": total_opportunities,
            "active_projects": active_projects,
            "running_pocs": running_pocs,
            "alerts_today": alerts_today,
            "alerts_critical": alerts_critical,
            "alerts_minor": alerts_minor,
            "total_active_sectors": len(set(t.domain_name for t in trends)),
            "total_technologies_tracked": len(set(tr.tech_name for tr in tech_radar)),
            "total_entities_tracked": len(entities)
        }
    }

@router.post("/calculate-trends", status_code=status.HTTP_202_ACCEPTED)
def trigger_trend_calculation(db: Session = Depends(get_db)):
    """
    Manually triggers the AI data aggregation for the dashboard.
    """
    AnalyticsService.calculate_daily_trends(db)
    AnalyticsService.calculate_tech_radar(db)
    AnalyticsService.calculate_entities(db)
    AnalyticsService.calculate_funnel(db)
    return {"message": "All dashboard calculations started successfully"}
