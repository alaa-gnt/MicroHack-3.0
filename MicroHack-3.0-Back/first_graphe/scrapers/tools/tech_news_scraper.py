"""
Tech news scraper - REAL scraping from tech news RSS feeds
Uses RSS feeds instead of HTML scraping (more reliable)
"""
from typing import List, Dict
import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .base_scraper import BaseScraperTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TechNewsScraperTool(BaseScraperTool):
    """
    Scrapes REAL tech news from RSS feeds
    """
    
    name = "scrape_tech_news"
    description = "Scrape tech news from TechCrunch, VentureBeat, etc."
    
    # RSS feeds for tech news (these are real, working feeds)
    TECH_FEEDS = {
        'techcrunch': 'https://techcrunch.com/feed/',
        'venturebeat': 'https://venturebeat.com/feed/',
        'wired': 'https://www.wired.com/feed/rss',
        'theverge': 'https://www.theverge.com/rss/index.xml',
        'arstechnica': 'https://feeds.arstechnica.com/arstechnica/index'
    }
    
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, topics: List[str] = None, sources: List[str] = None, days_back: int = 7) -> List[Dict]:
        """
        Scrape REAL tech news from RSS feeds
        
        Args:
            topics: Topics to filter by (optional)
            sources: Source names from TECH_FEEDS (default: all)
            days_back: Only articles from last N days
        
        Returns:
            List of REAL news articles
        """
        results = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        if sources is None:
            sources = ['techcrunch', 'venturebeat']  # Default sources
        
        logger.info(f"[TECH NEWS SCRAPER] Starting with {len(sources)} sources")
        
        for source in sources:
            source_lower = source.lower()
            feed_url = self.TECH_FEEDS.get(source_lower)
            
            if not feed_url:
                logger.warning(f"[TECH NEWS] Unknown source: {source}")
                continue
            
            try:
                logger.info(f"[TECH NEWS] Fetching: {source} ({feed_url})")
                
                response = requests.get(feed_url, headers=self.headers, timeout=30)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                
                if not feed.entries:
                    logger.warning(f"[TECH NEWS] No entries in {source}")
                    continue
                
                source_name = feed.feed.get('title', source.title())
                logger.info(f"[TECH NEWS] {source_name}: {len(feed.entries)} entries")
                
                articles_added = 0
                for entry in feed.entries[:15]:  # Limit per source
                    article = self._extract_article(entry, source_name, cutoff_date, topics)
                    if article:
                        results.append(article)
                        articles_added += 1
                
                logger.info(f"[TECH NEWS] Added {articles_added} articles from {source}")
                self._respect_rate_limit()
                
            except requests.RequestException as e:
                logger.error(f"[TECH NEWS] HTTP error for {source}: {str(e)}")
            except Exception as e:
                logger.error(f"[TECH NEWS] Error for {source}: {str(e)}")
        
        # Validate
        valid_results = [doc for doc in results if self._validate_document(doc)]
        
        logger.info(f"[TECH NEWS SCRAPER] Complete: {len(valid_results)} valid articles")
        return valid_results
    
    def _extract_article(self, entry, source_name: str, cutoff_date: datetime, topics: List[str] = None) -> Dict:
        """Extract article from RSS entry"""
        try:
            # Parse date
            pub_date = self._parse_date(entry)
            if pub_date and pub_date < cutoff_date:
                return None  # Skip old articles
            
            # Get basic info
            title = entry.get('title', '').strip()
            url = entry.get('link', '').strip()
            
            if not title or not url:
                return None
            
            # Filter by topics if specified
            if topics:
                title_lower = title.lower()
                content_lower = entry.get('summary', '').lower()
                matches = any(topic.lower() in title_lower or topic.lower() in content_lower 
                             for topic in topics)
                if not matches:
                    return None  # Skip if no topic match
            
            # Get content
            content = ''
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', '')
            if not content:
                content = entry.get('summary', '') or entry.get('description', '')
            
            # Clean HTML
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text(separator=' ', strip=True)
            
            # If content is too short, fetch the full article content
            if not content or len(content) < 300:
                logger.info(f"[TECH NEWS] Snippet too short for {url}, fetching full text...")
                full_text = self._fetch_full_text(url)
                if full_text:
                    content = full_text
            
            pub_date_str = pub_date.isoformat() if pub_date else datetime.now().isoformat()
            
            return {
                'url': url,
                'source': source_name,
                'title': title,
                'text': content[:5000],
                'published_date': pub_date_str
            }
            
        except Exception as e:
            logger.error(f"[TECH NEWS] Error extracting entry: {str(e)}")
            return None
    
    def _parse_date(self, entry) -> datetime:
        """Parse date from entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
        except:
            pass
        return datetime.now()