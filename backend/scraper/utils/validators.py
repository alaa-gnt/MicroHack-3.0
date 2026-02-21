"""
Validation utilities for the scraping system
"""
import re
from urllib.parse import urlparse
from typing import Optional


def is_valid_url(url: Optional[str]) -> bool:
    """
    Validate if a string is a valid URL
    
    Args:
        url: URL string to validate
    
    Returns:
        True if valid URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False


def is_valid_email(email: Optional[str]) -> bool:
    """
    Validate if a string is a valid email
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_date_string(date_str: Optional[str]) -> bool:
    """
    Validate if string looks like a date
    """
    if not date_str or not isinstance(date_str, str):
        return False
    
    # Common date patterns
    patterns = [
        r'^\d{4}-\d{2}-\d{2}',  # ISO format
        r'^\d{2}/\d{2}/\d{4}',  # US format
        r'^\d{2}-\d{2}-\d{4}',  # EU format
    ]
    
    return any(re.match(p, date_str) for p in patterns)


def validate_document(doc: dict) -> bool:
    """
    Validate a scraped document has required fields
    """
    required_fields = ['url', 'source', 'title', 'text', 'published_date']
    
    for field in required_fields:
        if not doc.get(field):
            return False
    
    if not is_valid_url(doc.get('url')):
        return False
    
    if len(doc.get('title', '')) < 5:
        return False
    
    if len(doc.get('text', '')) < 50:
        return False
    
    return True
