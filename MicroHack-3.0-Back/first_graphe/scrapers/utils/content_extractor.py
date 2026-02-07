"""
Advanced content extraction utilities
Extracts clean article text from various HTML structures
"""
from bs4 import BeautifulSoup
from typing import Optional
import re
from .soup_helper import SoupHelper

class ContentExtractor:
    """
    Extracts main article content from web pages
    """
    
    @staticmethod
    def extract_full_article(html_content: str) -> Optional[str]:
        """
        Extract full article text from HTML
        
        Returns:
            Clean article text or None
        """
        soup = SoupHelper.create_soup(html_content)
        
        # Remove ads and widgets
        soup = SoupHelper.remove_ads_and_widgets(soup)
        
        # Try to find article content
        article_text = SoupHelper.find_article_content(soup)
        
        if article_text and len(article_text) > 100:
            return ContentExtractor._clean_text(article_text)
        
        return None
    
    @staticmethod
    def extract_with_metadata(html_content: str) -> dict:
        """
        Extract article with metadata
        
        Returns:
            {
                'title': '...',
                'description': '...',
                'content': '...',
                'author': '...'
            }
        """
        soup = SoupHelper.create_soup(html_content)
        
        return {
            'title': ContentExtractor._extract_title(soup),
            'description': SoupHelper.find_meta_content(soup, 'description'),
            'content': SoupHelper.find_article_content(soup),
            'author': ContentExtractor._extract_author(soup)
        }
    
    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> Optional[str]:
        """Extract article title"""
        # Try <title> tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove site name (usually after | or -)
            title = re.split(r'\s+[-|]\s+', title)[0]
            return title
        
        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return None
    
    @staticmethod
    def _extract_author(soup: BeautifulSoup) -> Optional[str]:
        """Extract author name"""
        # Try meta tag
        author = SoupHelper.find_meta_content(soup, 'author')
        if author:
            return author
        
        # Try common author class
        author_element = soup.find(class_=lambda x: x and 'author' in x.lower())
        if author_element:
            return author_element.get_text(strip=True)
        
        return None
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean extracted text
        Remove extra whitespace, normalize line breaks
        """
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Remove multiple newlines (max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Strip
        text = text.strip()
        
        return text