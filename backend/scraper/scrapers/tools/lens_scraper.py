"""
Lens.org scraper - Alternative patent source
Uses public search interface for scraping patents
"""
from typing import List, Dict
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraperTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LensScraperTool(BaseScraperTool):
    """
    Scrapes patents from Lens.org
    Provides a fallback when Google Patents is blocked
    """
    
    name = "scrape_lens_patents"
    description = "Scrape patents from Lens.org"
    
    BASE_URL = "https://www.lens.org/lens/search/patent/list"
    
    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 3
    
    def scrape(self, keywords: List[str], days_back: int = 30) -> List[Dict]:
        """
        Scrape patents from Lens.org
        """
        results = []
        
        logger.info(f"[LENS SCRAPER] Starting with {len(keywords)} keywords")
        
        for keyword in keywords[:5]:
            try:
                self._respect_rate_limit()
                
                # Build search URL
                params = {
                    "q": keyword,
                    "preview": "true",
                    "sortField": "p_pub_date",
                    "sortDescending": "true"
                }
                
                # Fetch
                response = self.http_client.get(self.BASE_URL, params=params)
                if response.status_code != 200:
                    logger.warning(f"[LENS] Failed to fetch for '{keyword}': {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Parse results
                # Lens.org uses 'patent-record' class or similar
                items = soup.select('.patent-record') or soup.select('.search-result') or soup.select('article')
                
                logger.info(f"[LENS] Found {len(items)} potential items for: {keyword}")
                
                for item in items[:10]:
                    patent = self._extract_patent(item, keyword)
                    if patent:
                        results.append(patent)
                        
            except Exception as e:
                logger.error(f"[LENS] Error for '{keyword}': {str(e)}")
        
        # Deduplicate
        seen_urls = set()
        valid_results = []
        for doc in results:
            if doc['url'] not in seen_urls and self._validate_document(doc):
                seen_urls.add(doc['url'])
                valid_results.append(doc)
                
        logger.info(f"[LENS SCRAPER] Complete: {len(valid_results)} valid patents")
        return valid_results
    
    def _extract_patent(self, item, keyword: str) -> Dict:
        """Extract patent data from item"""
        try:
            link = item.find('a', href=re.compile(r'/lens/patent/'))
            if not link:
                return None
            
            href = link.get('href', '')
            url = f"https://www.lens.org{href}" if href.startswith('/') else href
            
            title_elem = item.find('h3') or item.find('h2') or link
            title = title_elem.get_text(strip=True)
            
            # Extract snippet
            snippet_elem = item.find('.abstract') or item.find('.description') or item.find('.snippet')
            text = snippet_elem.get_text(strip=True) if snippet_elem else ""
            if not text:
                text = item.get_text(separator=' ', strip=True)
            
            text = f"LENS PATENT DATA\n\nKEYWORD: {keyword}\n\nCONTENT:\n{text}"
            
            # Use current date if not found
            pub_date = datetime.now().isoformat()
            
            return {
                'url': url,
                'source': 'Lens.org',
                'title': title,
                'text': text[:5000],
                'published_date': pub_date
            }
        except Exception as e:
            logger.debug(f"[LENS] Extraction error: {e}")
            return None
