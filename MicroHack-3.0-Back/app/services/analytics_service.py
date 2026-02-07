from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List

from app.models.market_trend import MarketTrend
from app.models.technology_radar import TechnologyRadar
from app.models.entity_tracker import EntityTracker
from app.models.funnel_metric import FunnelMetric
from app.models.strategic_benchmark import StrategicBenchmark
from app.models.opportunity import Opportunity
from app.models.signal import Signal
from app.models.feasibility import FeasibilityStudy

class AnalyticsService:
    @staticmethod
    def calculate_daily_trends(db: Session):
        """
        Aggregates opportunities into daily domain trends.
        """
        today = date.today()
        
        # Aggregate data from Opportunity table grouped by domain
        stats = db.query(
            Opportunity.primary_domain,
            func.count(Opportunity.id).label("count"),
            func.avg(Opportunity.urgency_score).label("avg_urgency")
        ).group_by(Opportunity.primary_domain).all()

        for domain, count, avg_urgency in stats:
            # Check if trend for today already exists
            existing = db.query(MarketTrend).filter(
                MarketTrend.domain_name == domain,
                MarketTrend.snapshot_date == today
            ).first()

            if existing:
                existing.signal_count = count
                existing.avg_urgency_score = float(avg_urgency) if avg_urgency else 0.0
            else:
                new_trend = MarketTrend(
                    domain_name=domain,
                    signal_count=count,
                    avg_urgency_score=float(avg_urgency) if avg_urgency else 0.0,
                    snapshot_date=today
                )
                db.add(new_trend)
        
        db.commit()

    @staticmethod
    def get_market_trends(db: Session, limit: int = 30) -> List[MarketTrend]:
        return db.query(MarketTrend).order_by(MarketTrend.snapshot_date.desc()).limit(limit).all()

    @staticmethod
    def calculate_tech_radar(db: Session):
        """
        Aggregates technologies from opportunities to calculate maturity radar.
        """
        today = date.today()
        
        # Note: In a real app with comma-separated strings or arrays, 
        # this would involve more complex SQL or Python-side post-processing.
        # For now, we'll implement a basic aggregation.
        
        stats = db.query(
            Opportunity.technologies_mentioned,
            func.count(Opportunity.id).label("count"),
            func.avg(Opportunity.estimated_trl).label("avg_trl")
        ).filter(Opportunity.technologies_mentioned != None).group_by(Opportunity.technologies_mentioned).all()

        for tech_str, count, avg_trl in stats:
            # Simple handling for multiple techs in one string if needed
            # For now, we treat the exact string as the tech identifier
            techs = [t.strip() for t in tech_str.split(',')] if tech_str else []
            if not techs: continue

            for tech in techs:
                existing = db.query(TechnologyRadar).filter(
                    TechnologyRadar.tech_name == tech,
                    TechnologyRadar.snapshot_date == today
                ).first()

                if existing:
                    # Update (simplified: in a real split-scenario, we'd need a subquery for correct counts per tech)
                    existing.frequency_count += count
                    existing.avg_trl_level = float(avg_trl) if avg_trl else 0.0
                else:
                    new_radar = TechnologyRadar(
                        tech_name=tech,
                        frequency_count=count,
                        avg_trl_level=float(avg_trl) if avg_trl else 0.0,
                        snapshot_date=today
                    )
                    db.add(new_radar)
        
        db.commit()

    @staticmethod
    def get_tech_radar(db: Session, limit: int = 50) -> List[TechnologyRadar]:
        return db.query(TechnologyRadar).order_by(TechnologyRadar.snapshot_date.desc()).limit(limit).all()

    @staticmethod
    def calculate_entities(db: Session):
        """
        Aggregates companies and locations from opportunities.
        """
        # Clear old entity counts for a fresh snapshot
        # (In a larger app, we might want to keep history like trends)
        db.query(EntityTracker).delete()
        
        # 1. Process Companies
        company_stats = db.query(
            Opportunity.companies_mentioned,
            func.count(Opportunity.id).label("count"),
            func.avg(Opportunity.impact_score).label("avg_impact")
        ).filter(Opportunity.companies_mentioned != None).group_by(Opportunity.companies_mentioned).all()

        for comp_str, count, avg_impact in company_stats:
            comps = [c.strip() for c in comp_str.split(',')] if comp_str else []
            for comp in comps:
                existing = db.query(EntityTracker).filter(
                    EntityTracker.entity_name == comp,
                    EntityTracker.entity_type == 'Company'
                ).first()
                if existing:
                    existing.mention_count += count
                    existing.hotspot_score = (existing.hotspot_score + float(avg_impact)) / 2
                else:
                    db.add(EntityTracker(
                        entity_name=comp,
                        entity_type='Company',
                        mention_count=count,
                        hotspot_score=float(avg_impact) if avg_impact else 0.0
                    ))

        # 2. Process Locations
        location_stats = db.query(
            Opportunity.locations_mentioned,
            func.count(Opportunity.id).label("count"),
            func.avg(Opportunity.urgency_score).label("avg_urgency")
        ).filter(Opportunity.locations_mentioned != None).group_by(Opportunity.locations_mentioned).all()

        for loc_str, count, avg_urgency in location_stats:
            locs = [l.strip() for l in loc_str.split(',')] if loc_str else []
            for loc in locs:
                existing = db.query(EntityTracker).filter(
                    EntityTracker.entity_name == loc,
                    EntityTracker.entity_type == 'Location'
                ).first()
                if existing:
                    existing.mention_count += count
                    existing.hotspot_score = (existing.hotspot_score + float(avg_urgency)) / 2
                else:
                    db.add(EntityTracker(
                        entity_name=loc,
                        entity_type='Location',
                        mention_count=count,
                        hotspot_score=float(avg_urgency) if avg_urgency else 0.0
                    ))
        
        db.commit()

    @staticmethod
    def get_entities(db: Session, entity_type: str = None, limit: int = 100) -> List[EntityTracker]:
        query = db.query(EntityTracker)
        if entity_type:
            query = query.filter(EntityTracker.entity_type == entity_type)
        return query.order_by(EntityTracker.mention_count.desc()).limit(limit).all()

    @staticmethod
    def calculate_funnel(db: Session):
        """
        Calculates conversion rates through the pipeline stages.
        """
        today = date.today()
        # simplified 7-day window
        start_date = today # just a placeholder for now
        
        signal_count = db.query(func.count(Signal.id)).scalar() or 0
        opp_count = db.query(func.count(Opportunity.id)).scalar() or 0
        feas_count = db.query(func.count(FeasibilityStudy.id)).scalar() or 0

        # Stage 1: Signals
        db.add(FunnelMetric(
            stage="Signal",
            entry_count=signal_count,
            conversion_rate=100.0,
            period_start=today,
            period_end=today
        ))

        # Stage 2: Opportunities
        db.add(FunnelMetric(
            stage="Opportunity",
            entry_count=opp_count,
            conversion_rate=(opp_count / signal_count * 100) if signal_count > 0 else 0.0,
            period_start=today,
            period_end=today
        ))

        # Stage 3: Feasibility
        db.add(FunnelMetric(
            stage="Feasibility",
            entry_count=feas_count,
            conversion_rate=(feas_count / opp_count * 100) if opp_count > 0 else 0.0,
            period_start=today,
            period_end=today
        ))
        
        db.commit()

    @staticmethod
    def get_funnel(db: Session) -> List[FunnelMetric]:
        # Get latest stage metrics
        return db.query(FunnelMetric).order_by(FunnelMetric.id.desc()).limit(3).all()

    @staticmethod
    def get_benchmarks(db: Session) -> List[StrategicBenchmark]:
        return db.query(StrategicBenchmark).all()
