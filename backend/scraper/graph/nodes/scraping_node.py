"""
Scraping node - executes all scrapers and collects raw documents
Loads configuration dynamically from YAML files
"""
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from graph.state import GraphState
from scrapers.tools.patent_scraper import PatentScraperTool
from scrapers.tools.lens_scraper import LensScraperTool
from scrapers.tools.rss_scraper import RSSScraperTool
from scrapers.tools.tech_news_scraper import TechNewsScraperTool
from scrapers.tools.academic_scraper import AcademicScraperTool
from config.loader import get_scraping_config
from utils.logger import setup_logger
from storage.s3_client import s3_client
from monitoring.metrics import record_scraping_result
import uuid

logger = setup_logger(__name__)

def scraping_node(state: GraphState) -> GraphState:
    """
    Execute all scrapers in parallel and collect raw documents
    """
    documents = []
    
    # Load configuration from YAML files
    config = get_scraping_config()
    
    import random
    keywords = state.get("keywords") or config.get('keywords', [])
    # Shuffle keywords to ensure we don't always pick the same ones for the [:15] limit
    random_keywords = list(keywords)
    random.shuffle(random_keywords)
    rss_feeds = state.get("sources") or config.get('rss_feeds', [])
    tech_config = config.get('tech_news', {})
    academic_config = config.get('academic', {})
    
    logger.info("=" * 60)
    logger.info("SCRAPING NODE STARTED (PARALLEL MODE)")
    logger.info(f"Keywords: {len(keywords)}")
    logger.info(f"RSS Feeds: {len(rss_feeds)}")
    logger.info("=" * 60)
    
    def run_patent_scrapers():
        try:
            results = []
            
            # 1. Google Patents
            try:
                google_scraper = PatentScraperTool()
                # Use a larger sample of keywords, prioritized by type
                results.extend(google_scraper.run(keywords=random_keywords[:15], days_back=30))
            except Exception as e:
                logger.error(f"Google Patent scraper failed: {e}")
            
            # 2. Lens.org fallback
            if not results:
                logger.info("[SCRAPING] No results from Google Patents, trying Lens.org...")
                try:
                    lens_scraper = LensScraperTool()
                    results.extend(lens_scraper.run(keywords=random_keywords[:15], days_back=30))
                except Exception as e:
                    logger.error(f"Lens.org scraper failed: {e}")
            
            return results
        except Exception as e:
            logger.error(f"All patent scrapers failed: {e}")
            return []

    def run_rss_scraper():
        try:
            scraper = RSSScraperTool()
            return scraper.run(feed_urls=rss_feeds, days_back=7)
        except Exception as e:
            logger.error(f"RSS scraper failed: {e}")
            return []

    def run_tech_scraper():
        try:
            scraper = TechNewsScraperTool()
            topics = tech_config.get('topics', random_keywords[:15])
            sources = tech_config.get('sources', ['techcrunch', 'venturebeat'])
            return scraper.run(topics=topics, sources=sources, days_back=7)
        except Exception as e:
            logger.error(f"Tech news scraper failed: {e}")
            return []

    def run_academic_scraper():
        try:
            scraper = AcademicScraperTool()
            categories = academic_config.get('categories', ['cs.AI', 'cs.CY', 'cs.LG'])
            return scraper.run(keywords=random_keywords[:15], categories=categories, days_back=30)
        except Exception as e:
            logger.error(f"Academic scraper failed: {e}")
            return []

    # Run scrapers in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_patent_scrapers): "Patents",
            executor.submit(run_rss_scraper): "RSS",
            executor.submit(run_tech_scraper): "Tech News",
            executor.submit(run_academic_scraper): "Academic"
        }
        
        for future in futures:
            name = futures[future]
            try:
                docs = future.result()
                documents.extend(docs)
                logger.info(f"{name} scraper: {len(docs)} documents")
                
                # Record metrics
                record_scraping_result(name, len(docs))
                
                # Persist raw documents to S3
                for doc in docs:
                    doc_id = str(uuid.uuid4())
                    s3_client.upload_document(doc_id, doc)
            except Exception as e:
                logger.error(f"{name} scraper thread failed: {e}")

    logger.info("=" * 60)
    logger.info(f"TOTAL RAW DOCUMENTS COLLECTED: {len(documents)}")
    logger.info("=" * 60)
    
    return {
        "raw_documents": documents
    }
