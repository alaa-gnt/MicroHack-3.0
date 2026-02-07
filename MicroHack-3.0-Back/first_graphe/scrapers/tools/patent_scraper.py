"""
Patent scraper - REAL scraping from Google Patents using web scraping
Note: Google Patents doesn't have a public API, so we use web scraping
"""
from typing import List, Dict
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraperTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PatentScraperTool(BaseScraperTool):
    """
    Scrapes REAL patents from Google Patents
    Uses web scraping since there's no public API
    """
    
    name = "scrape_patents"
    description = "Scrape patents from Google Patents"
    
    BASE_URL = "https://patents.google.com"
    
    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 5  # Higher delay for Google to avoid bot detection
    
    def scrape(self, keywords: List[str], days_back: int = 30) -> List[Dict]:
        """
        Scrape REAL patents from Google Patents
        
        Args:
            keywords: Search keywords
            days_back: Patents from last N days
        
        Returns:
            List of REAL patent documents
        """
        results = []
        
        logger.info(f"[PATENT SCRAPER] Starting with {len(keywords)} keywords")
        
        for keyword in keywords[:5]:  # Limit to avoid rate limits
            try:
                self._respect_rate_limit()
                
                # Build search URL - simpler query often works better for bot protection
                search_url = f"{self.BASE_URL}/?q={requests.utils.quote(keyword)}"
                
                # Fetch using centralized HTTPClient
                response = self.http_client.get(search_url)
                
                if response.status_code == 429:
                    logger.warning("[PATENTS] Rate limited, skipping...")
                    continue
                
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find patent search results
                # Google Patents uses different structures, try multiple selectors
                patents = self._parse_search_results(soup, keyword)
                results.extend(patents)
                
                logger.info(f"[PATENTS] Found {len(patents)} patents for: {keyword}")
                
            except requests.RequestException as e:
                logger.error(f"[PATENTS] HTTP error for '{keyword}': {str(e)}")
            except Exception as e:
                logger.error(f"[PATENTS] Error for '{keyword}': {str(e)}")
        
        # Validate and deduplicate
        seen_urls = set()
        valid_results = []
        for doc in results:
            if doc['url'] not in seen_urls and self._validate_document(doc):
                seen_urls.add(doc['url'])
                valid_results.append(doc)
        
        logger.info(f"[PATENT SCRAPER] Complete: {len(valid_results)} valid patents")
        return valid_results
    
    def _parse_search_results(self, soup: BeautifulSoup, keyword: str) -> List[Dict]:
        """Parse patent search results from HTML"""
        results = []
        
        # Try to find patent result items
        # Google Patents structure can vary
        
        # Look for search result items - modern Google Patents selectors
        result_items = soup.select('section.search-result-item')
        
        if not result_items:
            result_items = soup.find_all('search-result-item')
        
        if not result_items:
            # Alternative: look for article elements
            result_items = soup.find_all('article')
        
        if not result_items:
            # Alternative: look for elements with [data-result]
            result_items = soup.select('[data-result]')
        
        logger.info(f"[PATENTS] Found {len(result_items)} potential result items")
        
        for item in result_items[:10]:  # Limit per keyword
            try:
                patent = self._extract_patent_from_item(item, keyword)
                if patent:
                    results.append(patent)
            except Exception as e:
                logger.error(f"[PATENTS] Error parsing item: {str(e)}")
                continue
        
        # If no structured results, try to extract from page text
        if not results:
            results = self._extract_from_page_text(soup, keyword)
        
        return results
    
    def _extract_patent_from_item(self, item, keyword: str) -> Dict:
        """Extract patent data from search result item"""
        try:
            # Find link
            link = item.find('a', href=True)
            if not link:
                return None
            
            href = link.get('href', '')
            if not href.startswith('/patent/'):
                # Try to find patent link in nested elements
                patent_link = item.find('a', href=re.compile(r'/patent/'))
                if patent_link:
                    href = patent_link.get('href', '')
            
            if not href:
                return None
            
            patent_url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
            
            # Extract patent ID from URL
            patent_id_match = re.search(r'/patent/([A-Z0-9]+)', href)
            patent_id = patent_id_match.group(1) if patent_id_match else "Unknown"
            
            # Find title
            title = None
            title_elem = item.find('h3') or item.find('h4') or item.find(class_=re.compile(r'title'))
            if title_elem:
                title = title_elem.get_text(strip=True)
            if not title:
                title = link.get_text(strip=True)
            if not title:
                title = f"Patent {patent_id}"
            
            # Find abstract/snippet
            text = ""
            snippet_elem = item.find(class_=re.compile(r'snippet|abstract|description'))
            if snippet_elem:
                text = snippet_elem.get_text(strip=True)
            if not text:
                # Get all text from item
                text = item.get_text(separator=' ', strip=True)
            
            # Clean up text
            text = f"PATENT ID: {patent_id}\n\nKEYWORD: {keyword}\n\nCONTENT:\n{text[:2000]}"
            
            # Date - try to find or use current date
            date_elem = item.find('time') or item.find(class_=re.compile(r'date'))
            pub_date = date_elem.get('datetime', '') if date_elem else datetime.now().isoformat()
            
            return {
                'url': patent_url,
                'source': 'Google Patents',
                'title': title,
                'text': text,
                'published_date': pub_date if pub_date else datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"[PATENTS] Error extracting patent: {str(e)}")
            return None
    
    def _extract_from_page_text(self, soup: BeautifulSoup, keyword: str) -> List[Dict]:
        """Fallback: extract any patent references from page"""
        results = []
        
        # Find all links that look like patent links
        patent_links = soup.find_all('a', href=re.compile(r'/patent/[A-Z0-9]+'))
        
        for link in patent_links[:5]:
            href = link.get('href', '')
            patent_url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
            
            patent_id_match = re.search(r'/patent/([A-Z0-9]+)', href)
            patent_id = patent_id_match.group(1) if patent_id_match else "Unknown"
            
            title = link.get_text(strip=True) or f"Patent {patent_id}"
            
            results.append({
                'url': patent_url,
                'source': 'Google Patents',
                'title': title,
                'text': f"Patent {patent_id} related to: {keyword}. Visit {patent_url} for full details.",
                'published_date': datetime.now().isoformat()
            })
        
        return results