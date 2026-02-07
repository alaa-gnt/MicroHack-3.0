"""
Base scraper class with common functionality
All scrapers inherit from this
NOTE: Using custom base class instead of LangChain BaseTool to avoid Pydantic issues
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
from datetime import datetime
from bs4 import BeautifulSoup
from utils.logger import setup_logger
from scrapers.utils.http_client import HTTPClient

logger = setup_logger(__name__)


class BaseScraperTool(ABC):
    """
    Base class for all scraping tools
    Provides retry logic, error handling, rate limiting
    """
    
    # Subclasses should override these
    name: str = "base_scraper"
    description: str = "Base scraper tool"
    
    def __init__(self):
        self.http_client = HTTPClient(timeout=30, max_retries=3)
        self.rate_limit_delay = 1  # seconds between requests
        self.headers = self.http_client.session.headers  # Reference HTTPClient headers
    
    @abstractmethod
    def scrape(self, **kwargs) -> List[Dict]:
        """
        Each scraper implements this method
        
        Returns:
            List of documents with format:
            {
                'url': '...',
                'source': '...',
                'title': '...',
                'text': '...',
                'published_date': '...'
            }
        """
        pass
    
    def run(self, **kwargs) -> List[Dict]:
        """
        Main entry point - wraps scrape() with error handling
        """
        try:
            logger.info(f"Starting {self.name} with params: {kwargs}")
            results = self.scrape(**kwargs)
            logger.info(f"{self.name} completed: {len(results)} documents found")
            return results
            
        except Exception as e:
            logger.error(f"{self.name} failed: {str(e)}")
            return []
    
    def _respect_rate_limit(self):
        """Sleep to respect rate limits"""
        time.sleep(self.rate_limit_delay)
    
    def _fetch_full_text(self, url: str) -> str:
        """
        Fetch full text from a URL by scraping the HTML
        """
        try:
            response = self.http_client.get(url)
            if response.status_code != 200:
                return ""
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Find main content (heuristic: look for article, main, or long paragraphs)
            article = soup.find('article') or soup.find('main')
            
            if article:
                text = article.get_text(separator=' ', strip=True)
            else:
                # Fallback: get all text from paragraphs
                paragraphs = soup.find_all('p')
                text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Clean up text
            text = ' '.join(text.split())
            return text[:10000]  # Limit total length
                
        except Exception as e:
            logger.error(f"Error fetching full text from {url}: {e}")
            return ""

    def _validate_document(self, doc: Dict) -> bool:
        """
        Validate document has required fields
        """
        required_fields = ['url', 'source', 'title', 'text', 'published_date']
        
        for field in required_fields:
            if field not in doc or not doc[field]:
                logger.warning(f"Document missing field: {field}")
                return False
        
        # Check minimum lengths
        if len(doc['title']) < 5:
            logger.warning("Title too short")
            return False
        
        if len(doc['text']) < 50:
            logger.warning("Text too short")
            return False
        
        return True