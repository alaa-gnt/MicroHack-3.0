"""
Academic paper scraper - REAL scraping from arXiv API
arXiv provides a free, public API that returns real paper data
"""
from typing import List, Dict
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraperTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AcademicScraperTool(BaseScraperTool):
    """
    Scrapes REAL academic papers from arXiv API
    arXiv is free and doesn't require API key
    """
    
    name = "scrape_academic_papers"
    description = "Scrape academic papers from arXiv"
    
    ARXIV_API_URL = "http://export.arxiv.org/api/query"
    
    def scrape(self, keywords: List[str], categories: List[str] = None, days_back: int = 30) -> List[Dict]:
        """
        Scrape REAL papers from arXiv
        
        Args:
            keywords: Search keywords
            categories: arXiv categories (e.g., ["cs.AI", "cs.CY"])
            days_back: Papers from last N days
        
        Returns:
            List of REAL paper documents from arXiv
        """
        results = []
        
        if categories is None:
            categories = ["cs.AI", "cs.CY", "cs.LG"]
        
        logger.info(f"[ACADEMIC SCRAPER] Starting with {len(keywords)} keywords")
        
        for keyword in keywords[:5]:  # Limit keywords to avoid rate limits
            try:
                self._respect_rate_limit()
                
                # Build arXiv query
                # Search in title and abstract
                query = f'all:"{keyword}"'
                
                # Add category filter if specified
                if categories:
                    cat_query = ' OR '.join([f'cat:{cat}' for cat in categories])
                    query = f'({query}) AND ({cat_query})'
                
                params = {
                    'search_query': query,
                    'start': 0,
                    'max_results': 20,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                logger.info(f"[ARXIV] Searching for: {keyword}")
                
                response = requests.get(
                    self.ARXIV_API_URL,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse XML response
                soup = BeautifulSoup(response.text, 'xml')
                entries = soup.find_all('entry')
                
                logger.info(f"[ARXIV] Found {len(entries)} papers for: {keyword}")
                
                for entry in entries:
                    paper = self._parse_arxiv_entry(entry, days_back)
                    if paper:
                        results.append(paper)
                
            except requests.RequestException as e:
                logger.error(f"[ARXIV] HTTP error for '{keyword}': {str(e)}")
            except Exception as e:
                logger.error(f"[ARXIV] Error for '{keyword}': {str(e)}")
        
        # Validate and deduplicate by URL
        seen_urls = set()
        valid_results = []
        for doc in results:
            if doc['url'] not in seen_urls and self._validate_document(doc):
                seen_urls.add(doc['url'])
                valid_results.append(doc)
        
        logger.info(f"[ACADEMIC SCRAPER] Complete: {len(valid_results)} valid papers")
        return valid_results
    
    def _parse_arxiv_entry(self, entry, days_back: int) -> Dict:
        """Parse arXiv XML entry into document"""
        try:
            # Extract ID (used as URL)
            id_elem = entry.find('id')
            arxiv_url = id_elem.get_text(strip=True) if id_elem else None
            if not arxiv_url:
                return None
            
            # Extract title
            title_elem = entry.find('title')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            # Clean up title (remove newlines)
            title = ' '.join(title.split())
            
            # Extract abstract
            abstract_elem = entry.find('summary')
            abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""
            abstract = ' '.join(abstract.split())  # Clean whitespace
            
            # Extract publication date
            published_elem = entry.find('published')
            published_str = published_elem.get_text(strip=True) if published_elem else ""
            
            # Check date is within range
            try:
                pub_date = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                cutoff = datetime.now(pub_date.tzinfo) - timedelta(days=days_back)
                if pub_date < cutoff:
                    return None  # Skip old papers
            except:
                pass  # Keep paper if we can't parse date
            
            # Extract authors
            authors = []
            for author in entry.find_all('author'):
                name_elem = author.find('name')
                if name_elem:
                    authors.append(name_elem.get_text(strip=True))
            authors_str = ', '.join(authors[:5])  # Limit to 5 authors
            if len(authors) > 5:
                authors_str += f" et al. ({len(authors)} authors)"
            
            # Extract categories
            categories = []
            for cat in entry.find_all('category'):
                term = cat.get('term')
                if term:
                    categories.append(term)
            categories_str = ', '.join(categories[:3])
            
            # Build full text
            text = f"TITLE: {title}\n\n"
            text += f"AUTHORS: {authors_str}\n\n"
            text += f"CATEGORIES: {categories_str}\n\n"
            text += f"ABSTRACT:\n{abstract}"
            
            return {
                'url': arxiv_url,
                'source': 'arXiv',
                'title': title,
                'text': text,
                'published_date': published_str
            }
            
        except Exception as e:
            logger.error(f"[ARXIV] Error parsing entry: {str(e)}")
            return None