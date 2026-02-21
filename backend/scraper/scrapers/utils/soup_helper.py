"""
BeautifulSoup helper utilities
Common parsing functions
"""
from bs4 import BeautifulSoup
from typing import Optional, List
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SoupHelper:
    """
    Helper class for BeautifulSoup operations
    """
    
    @staticmethod
    def create_soup(html_content: str, parser: str = "html.parser") -> BeautifulSoup:
        """
        Create BeautifulSoup object
        
        Args:
            html_content: HTML string
            parser: Parser to use (html.parser, lxml, html5lib)
        
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, parser)
    
    @staticmethod
    def find_article_content(soup: BeautifulSoup) -> Optional[str]:
        """
        Extract article content from common HTML structures
        
        Tries common article selectors:
        - <article> tag
        - div with class containing 'content', 'article', 'post'
        - <main> tag
        """
        # Try <article> tag first
        article = soup.find('article')
        if article:
            return SoupHelper.extract_text(article)
        
        # Try common content divs
        content_selectors = [
            {'class_': lambda x: x and 'article-content' in x.lower()},
            {'class_': lambda x: x and 'post-content' in x.lower()},
            {'class_': lambda x: x and 'entry-content' in x.lower()},
            {'class_': lambda x: x and 'main-content' in x.lower()},
        ]
        
        for selector in content_selectors:
            content_div = soup.find('div', selector)
            if content_div:
                return SoupHelper.extract_text(content_div)
        
        # Try <main> tag
        main = soup.find('main')
        if main:
            return SoupHelper.extract_text(main)
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        return None
    
    @staticmethod
    def extract_text(element: BeautifulSoup) -> str:
        """
        Extract clean text from BeautifulSoup element
        Removes scripts, styles, navigation, etc.
        """
        # Remove unwanted tags
        for tag in element.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            tag.decompose()
        
        # Get text
        text = element.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]  # Remove empty lines
        
        return '\n\n'.join(lines)
    
    @staticmethod
    def find_meta_content(soup: BeautifulSoup, meta_name: str) -> Optional[str]:
        """
        Extract content from meta tag
        
        Example: find_meta_content(soup, 'description')
        """
        meta = soup.find('meta', attrs={'name': meta_name})
        if meta and meta.get('content'):
            return meta.get('content')
        
        # Try property attribute (for og: tags)
        meta = soup.find('meta', attrs={'property': meta_name})
        if meta and meta.get('content'):
            return meta.get('content')
        
        return None
    
    @staticmethod
    def remove_ads_and_widgets(soup: BeautifulSoup) -> BeautifulSoup:
        """
        Remove common ad and widget elements
        """
        # Common ad/widget selectors
        unwanted_selectors = [
            {'class_': lambda x: x and 'ad' in x.lower()},
            {'class_': lambda x: x and 'advertisement' in x.lower()},
            {'class_': lambda x: x and 'sidebar' in x.lower()},
            {'class_': lambda x: x and 'widget' in x.lower()},
            {'id': lambda x: x and 'ad' in x.lower()},
        ]
        
        for selector in unwanted_selectors:
            for element in soup.find_all('div', selector):
                element.decompose()
        
        return soup