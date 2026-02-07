"""
Celery tasks for the scraping workflow
"""
from scheduler.celery_app import celery_app
from graph.workflow import build_scraping_graph
from graph.state import GraphState
from config.loader import get_scraping_config
from utils.logger import setup_logger
from utils.timestamp import now_iso8601
from utils.uuid_generator import generate_uuid

logger = setup_logger(__name__)


@celery_app.task(bind=True, name='scheduler.tasks.run_scraping_workflow')
def run_scraping_workflow(self):
    """
    Main task to run the complete scraping workflow
    This is scheduled to run every 5 hours
    """
    logger.info("=" * 60)
    logger.info("SCHEDULED SCRAPING WORKFLOW STARTED")
    logger.info(f"Time: {now_iso8601()}")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = get_scraping_config()
        
        # Build and run the graph
        app = build_scraping_graph()
        
        # Initial state with config
        initial_state = GraphState(
            batch_id=generate_uuid(),
            action="scrape",
            sources=config.get('rss_feeds', []),
            keywords=config.get('keywords', []),
            signals=[]
        )
        
        # Run the workflow
        result = app.invoke(initial_state)
        
        # Log results
        signals_count = len(result.get('signals', []))
        batch_id = result.get('batch_id', 'unknown')
        
        logger.info("=" * 60)
        logger.info("SCRAPING WORKFLOW COMPLETED")
        logger.info(f"Batch ID: {batch_id}")
        logger.info(f"Signals Generated: {signals_count}")
        logger.info("=" * 60)
        
        return {
            'status': 'success',
            'batch_id': batch_id,
            'signals_count': signals_count,
            'timestamp': now_iso8601()
        }
        
    except Exception as e:
        logger.error(f"Scraping workflow failed: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': now_iso8601()
        }


@celery_app.task(name='scheduler.tasks.run_single_scraper')
def run_single_scraper(scraper_type: str, **kwargs):
    """
    Run a single scraper for testing
    
    Args:
        scraper_type: 'patent', 'rss', 'tech_news', or 'academic'
    """
    logger.info(f"Running single scraper: {scraper_type}")
    
    try:
        if scraper_type == 'patent':
            from scrapers.tools.patent_scraper import PatentScraperTool
            scraper = PatentScraperTool()
        elif scraper_type == 'rss':
            from scrapers.tools.rss_scraper import RSSScraperTool
            scraper = RSSScraperTool()
        elif scraper_type == 'tech_news':
            from scrapers.tools.tech_news_scraper import TechNewsScraperTool
            scraper = TechNewsScraperTool()
        elif scraper_type == 'academic':
            from scrapers.tools.academic_scraper import AcademicScraperTool
            scraper = AcademicScraperTool()
        else:
            return {'status': 'error', 'error': f'Unknown scraper type: {scraper_type}'}
        
        results = scraper.run(**kwargs)
        
        return {
            'status': 'success',
            'scraper': scraper_type,
            'documents_count': len(results),
            'documents': results
        }
        
    except Exception as e:
        logger.error(f"Single scraper failed: {str(e)}")
        return {'status': 'error', 'error': str(e)}
