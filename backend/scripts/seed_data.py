"""
Seed data script to populate the database with real sample data.
"""
import sys
import os
from datetime import datetime, timedelta, date

# Ensure the parent directory of 'app' is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from app.database.postgres import SessionLocal
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.alert import Alert
from app.models.strategic_benchmark import StrategicBenchmark
from app.models.feasibility import FeasibilityStudy
from app.models.market_trend import MarketTrend
from app.models.technology_radar import TechnologyRadar
from app.models.entity_tracker import EntityTracker
from app.models.funnel_metric import FunnelMetric
from app.services.analytics_service import AnalyticsService

def seed():
    db = SessionLocal()
    try:
        print("Cleaning up existing data...")
        # Clear existing data in correct order due to FKs
        db.query(Alert).delete()
        db.query(FunnelMetric).delete()
        db.query(MarketTrend).delete()
        db.query(TechnologyRadar).delete()
        db.query(EntityTracker).delete()
        db.query(FeasibilityStudy).delete()
        db.query(Opportunity).delete()
        db.query(Signal).delete()
        db.query(StrategicBenchmark).delete()
        db.commit()

        print("Seeding signals and opportunities...")
        
        # Sample 1: AI Port Management
        s1 = Signal(
            title="AI-Driven Autonomous Port Management System",
            full_content="New research shows that AI can optimize port vessel traffic by 40% using real-time sensor data and predictive modeling.",
            source_url="https://techcrunch.com/ai-ports",
            source_name="TechCrunch",
            date=datetime.utcnow() - timedelta(hours=2),
            is_processed=True
        )
        db.add(s1)
        db.flush() # Get ID
        
        o1 = Opportunity(
            signal_id=s1.id,
            primary_domain="AI",
            urgency_score=85,
            impact_score=90,
            estimated_trl=4,
            companies_mentioned="PortMaster AI, DeepBlue Logistics",
            technologies_mentioned="Predictive ML, Computer Vision",
            locations_mentioned="Singapore, Rotterdam"
        )
        db.add(o1)
        db.flush()

        # Sample 2: Blockchain Cargo
        s2 = Signal(
            title="Blockchain implementation for global cargo tracking",
            full_content="A new consortium of shipping companies is adopting blockchain to reduce paperwork and improve transparency in cross-border trade.",
            source_url="https://reuters.com/blockchain-cargo",
            source_name="Reuters",
            date=datetime.utcnow() - timedelta(hours=5),
            is_processed=True
        )
        db.add(s2)
        db.flush()
        
        o2 = Opportunity(
            signal_id=s2.id,
            primary_domain="Blockchain",
            urgency_score=70,
            impact_score=85,
            estimated_trl=6,
            companies_mentioned="TradeLens, FedEx",
            technologies_mentioned="Hyperledger, Smart Contracts",
            locations_mentioned="Global"
        )
        db.add(o2)

        # Sample 3: IoT Smart Warehouse
        s3 = Signal(
            title="Next-generation IoT sensors for cold chain monitoring",
            full_content="New ultra-low power IoT sensors can monitor temperature variations in medicine shipments with 0.01 degree precision.",
            source_name="IoT World",
            date=datetime.utcnow() - timedelta(days=1),
            is_processed=True
        )
        db.add(s3)
        db.flush()
        
        o3 = Opportunity(
            signal_id=s3.id,
            primary_domain="IoT",
            urgency_score=95,
            impact_score=75,
            estimated_trl=8,
            companies_mentioned="SensorCloud",
            technologies_mentioned="NB-IoT, Edge Computing",
            locations_mentioned="Germany"
        )
        db.add(o3)
        db.flush()

        print("Seeding feasibility studies...")
        f1 = FeasibilityStudy(
            opportunity_id=o1.id,
            technical_assessment="High feasibility using existing NLP models.",
            required_technology_stack="Python, PyTorch, Docker",
            market_analysis="Strong demand in Asian ports.",
            overall_feasibility="High",
            final_recommendation="Approve"
        )
        db.add(f1)

        print("Seeding alerts...")
        a1 = Alert(
            opportunity_id=o1.id,
            title="Critical Opportunity Detected",
            message="Critical high-impact AI opportunity detected in Singapore",
            severity="High",
            is_read=False
        )
        db.add(a1)
        
        a2 = Alert(
            opportunity_id=o3.id,
            title="Urgent Cold Chain Breakthrough",
            message="Urgent IoT cold chain breakthrough requires immediate review",
            severity="Critical",
            is_read=False
        )
        db.add(a2)

        print("Seeding benchmarks...")
        b1 = StrategicBenchmark(
            sector="Logistics",
            metric_name="AI Adoption Level",
            benchmark_value=60.0,
            unit="Percentage"
        )
        db.add(b1)

        db.commit()
        
        print("Calculating analytics...")
        AnalyticsService.calculate_daily_trends(db)
        AnalyticsService.calculate_tech_radar(db)
        AnalyticsService.calculate_entities(db)
        AnalyticsService.calculate_funnel(db)
        
        print("✅ Seeding completed successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
