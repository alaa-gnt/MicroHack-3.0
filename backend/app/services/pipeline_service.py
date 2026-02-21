import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.feasibility import FeasibilityStudy

class PipelineService:
    @staticmethod
    def run_scraping_pipeline(db: Session, keywords: list = None, sources: list = None):
        """
        Orchestrates the scraping agent workflow.
        """
        # Ensure first_graphe and its parent are in the python path
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        agent_dir = os.path.join(base_dir, "first_graphe")
        
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
        if agent_dir not in sys.path:
            sys.path.insert(0, agent_dir)
            
        try:
            # Import agent workflow inside the method to avoid circular imports 
            # and ensure sys.path is updated
            from graph.workflow import build_scraping_graph
            
            # Build and run the graph
            scraping_graph = build_scraping_graph()
            
            # Prepare initial state
            initial_state = {
                "action": "scrape",
                "sources": sources or ["techcrunch", "theverge", "wired"],
                "keywords": keywords or ["AI", "Innovation", "Market Trends"],
                "batch_id": f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            }
            
            # Invoke the LangGraph workflow
            # The handoff_node inside the graph will handle saving to DB
            result = scraping_graph.invoke(initial_state)
            return result
            
        except ImportError as e:
            print(f"Import Error: {e}")
            return {"error": f"Could not load scraping agent: {str(e)}"}
        except Exception as e:
            print(f"Error running scraping pipeline: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_pipeline_overview(db: Session):
        """
        Retrieves counts for each pipeline stage and a list of most recent projects.
        """
        # 1. Calculate Stage Counts
        signals_count = db.query(func.count(Signal.id)).filter(Signal.is_processed == False).scalar() or 0
        opp_count = db.query(func.count(Opportunity.id)).scalar() or 0
        feas_count = db.query(func.count(FeasibilityStudy.id)).scalar() or 0
        
        stages = [
            {"id": "signals", "name": "Signals", "count": signals_count},
            {"id": "opportunity-sheet", "name": "Opportunity sheet", "count": opp_count},
            {"id": "feasibility-study", "name": "Feasibility Study", "count": feas_count},
            {"id": "poc", "name": "POC", "count": 0},
            {"id": "project", "name": "Project", "count": 0},
        ]

        # 2. Get Recent Projects (Combined from available stages)
        # For simplicity, we'll take top 3 from each main stage
        recent = []
        
        # Signals
        sigs = db.query(Signal).filter(Signal.is_processed == False).order_by(Signal.date.desc()).limit(3).all()
        for s in sigs:
            recent.append({
                "id": s.id,
                "stage": "signals",
                "stageName": "Signal",
                "title": s.title,
                "description": s.full_content[:150] + "..." if s.full_content else "",
                "source": s.source_name,
                "status": "New",
                "statusColor": "orange",
                "timestamp": s.date.isoformat(),
                "actionLabel": "Review Signal"
            })
            
        # Opportunities
        opps = db.query(Opportunity).join(Signal).order_by(Signal.date.desc()).limit(3).all()
        for o in opps:
            recent.append({
                "id": o.id,
                "stage": "opportunity-sheet",
                "stageName": "Opportunity",
                "title": o.signal.title,
                "description": f"Analysis for {o.primary_domain}",
                "source": o.signal.source_name,
                "status": "Analyzed",
                "statusColor": "blue",
                "timestamp": o.signal.date.isoformat(),
                "actionLabel": "View Opportunity"
            })

        return {
            "stages": stages,
            "recentProjects": sorted(recent, key=lambda x: x['timestamp'], reverse=True)[:10]
        }

    @staticmethod
    def get_stage_projects(db: Session, stage_id: str):
        """
        Returns projects (normalized items) for a specific stage.
        """
        projects = []
        
        if stage_id == "signals":
            items = db.query(Signal).filter(Signal.is_processed == False).order_by(Signal.date.desc()).all()
            for item in items:
                projects.append({
                    "id": item.id,
                    "title": item.title,
                    "description": item.full_content[:200] + "..." if item.full_content else "",
                    "source": item.source_name,
                    "status": "New",
                    "statusColor": "orange",
                    "timestamp": item.date.isoformat(),
                    "actionLabel": "Review Signal"
                })
        
        elif stage_id == "opportunity-sheet":
            items = db.query(Opportunity).join(Signal).order_by(Signal.date.desc()).all()
            for item in items:
                projects.append({
                    "id": item.id,
                    "title": item.signal.title,
                    "description": f"Domain: {item.primary_domain}. Impact: {item.impact_score}. Urgency: {item.urgency_score}",
                    "source": item.signal.source_name,
                    "status": "Ready to advance",
                    "statusColor": "blue",
                    "timestamp": item.signal.date.isoformat(),
                    "actionLabel": "View Opportunity"
                })
                
        elif stage_id == "feasibility-study":
            items = db.query(FeasibilityStudy).join(Opportunity).join(Signal).order_by(Signal.date.desc()).all()
            for item in items:
                projects.append({
                    "id": item.id,
                    "title": item.opportunity.signal.title,
                    "description": f"Recommendation: {item.final_recommendation}. Result: {item.overall_feasibility}",
                    "source": item.opportunity.signal.source_name,
                    "status": "Evaluated",
                    "statusColor": "green",
                    "timestamp": item.opportunity.signal.date.isoformat(),
                    "actionLabel": "View Study"
                })

        return {"projects": projects}
