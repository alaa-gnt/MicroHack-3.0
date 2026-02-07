"""
RSS feed scraper - REAL scraping from live RSS feeds
Uses feedparser for RSS parsing and requests for fetching
"""
from typing import List, Dict
import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .base_scraper import BaseScraperTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RSSScraperTool(BaseScraperTool):
    """
    Scrapes REAL RSS feeds and extracts articles
    """
    
    name = "scrape_rss_feeds"
    description = "Scrape RSS feeds from maritime and port technology sites"
    
    def __init__(self):
        super().__init__()
        # Specializing headers for RSS feeds
        self.headers.update({
            'Accept': 'application/rss+xml,application/xml;q=0.9,text/xml;q=0.8,*/*;q=0.7'
        })
    
    def scrape(self, feed_urls: List[str], days_back: int = 7) -> List[Dict]:
        """
        Scrape REAL RSS feeds
        
        Args:
            feed_urls: List of RSS feed URLs to scrape
            days_back: Only include articles from last N days
        
        Returns:
            List of article documents with real data
        """
        results = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        logger.info(f"[RSS SCRAPER] Starting with {len(feed_urls)} feeds")
        
        for feed_url in feed_urls:
            try:
                # Fetch RSS feed using centralized HTTPClient
                response = self.http_client.get(feed_url)
                
                # Parse RSS feed
                feed = feedparser.parse(response.content)
                
                if feed.bozo and not feed.entries:
                    logger.warning(f"[RSS] Feed has errors or empty (bozo: {feed.bozo}): {feed_url}")
                    continue
                
                # Get source name
                source_name = feed.feed.get('title', 'Unknown Source')
                logger.info(f"[RSS] Source: {source_name} - Found {len(feed.entries)} entries")
                
                # Process entries
                for entry in feed.entries[:20]:  # Limit to 20 per feed
                    article = self._extract_article(entry, source_name, cutoff_date)
                    if article:
                        results.append(article)
                
                self._respect_rate_limit()
                
            except requests.RequestException as e:
                logger.error(f"[RSS] HTTP error for {feed_url}: {str(e)}")
            except Exception as e:
                logger.error(f"[RSS] Error for {feed_url}: {str(e)}")
        
        # Validate all documents
        valid_results = [doc for doc in results if self._validate_document(doc)]
        
        logger.info(f"[RSS SCRAPER] Complete: {len(valid_results)} valid articles from {len(feed_urls)} feeds")
        return valid_results
    
    def _extract_article(self, entry, source_name: str, cutoff_date: datetime) -> Dict:
        """Extract article from RSS entry"""
        try:
            # Get publication date
            pub_date = self._parse_date(entry)
            if pub_date and pub_date < cutoff_date:
                return None  # Skip old articles
            
            # Get basic info
            title = entry.get('title', '').strip()
            url = entry.get('link', '').strip()
            
            if not title or not url:
                return None
            
            # Get content - try multiple fields
            content = ''
            
            # Try content:encoded first (usually full content)
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', '')
            
            # Fallback to summary/description
            if not content:
                content = entry.get('summary', '') or entry.get('description', '')
            
            # Clean HTML from content
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text(separator=' ', strip=True)
            
            # If content is too short, try to fetch the full page content
            if not content or len(content) < 300:
                logger.info(f"[RSS] Snippet too short for {url}, fetching full text...")
                full_text = self._fetch_full_text(url)
                if full_text:
                    content = full_text
                elif not content:
                    content = title  # Fallback to title if both fail
            
            pub_date_str = pub_date.isoformat() if pub_date else datetime.now().isoformat()
            
            return {
                'url': url,
                'source': source_name,
                'title': title,
                'text': content[:5000],  # Limit text length
                'published_date': pub_date_str
            }
            
        except Exception as e:
            logger.error(f"[RSS] Error extracting entry: {str(e)}")
            return None
    
    def _parse_date(self, entry) -> datetime:
        """Parse date from RSS entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
        except:
            pass
        return datetime.now()