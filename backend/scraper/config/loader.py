"""
Configuration loader - loads keywords and sources from YAML files
"""
import os
import yaml
from typing import List, Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Config directory path
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


def load_yaml(filename: str) -> Dict:
    """Load YAML file from config directory"""
    filepath = os.path.join(CONFIG_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return {}


def get_all_keywords() -> List[str]:
    """
    Get all keywords from keywords.yaml
    Returns flat list of all keywords from all categories
    """
    config = load_yaml('keywords.yaml')
    keywords = []
    
    # Primary keywords (nested by category)
    primary = config.get('primary_keywords', {})
    for category, keyword_list in primary.items():
        if isinstance(keyword_list, list):
            keywords.extend(keyword_list)
    
    # Port operations keywords (flat list)
    port_ops = config.get('port_operations', [])
    if isinstance(port_ops, list):
        keywords.extend(port_ops)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw.lower() not in seen:
            seen.add(kw.lower())
            unique_keywords.append(kw)
    
    logger.info(f"Loaded {len(unique_keywords)} unique keywords from config")
    return unique_keywords


def get_rss_feeds() -> List[str]:
    """
    Get all enabled RSS feed URLs from sources.yaml
    """
    config = load_yaml('sources.yaml')
    feeds = []
    
    rss_feeds = config.get('rss_feeds', [])
    for feed in rss_feeds:
        if isinstance(feed, dict) and feed.get('enabled', True):
            url = feed.get('url')
            if url:
                feeds.append(url)
    
    logger.info(f"Loaded {len(feeds)} RSS feeds from config")
    return feeds


def get_tech_news_config() -> Dict:
    """
    Get tech news sources configuration
    Returns dict with topics and enabled sources
    """
    config = load_yaml('sources.yaml')
    tech_news = config.get('tech_news', {})
    
    sources = []
    topics = []
    
    for source_name, source_config in tech_news.items():
        if isinstance(source_config, dict) and source_config.get('enabled', True):
            sources.append(source_name)
            topics.extend(source_config.get('search_topics', []))
    
    # Remove duplicate topics
    topics = list(set(topics))
    
    logger.info(f"Loaded tech news config: {len(sources)} sources, {len(topics)} topics")
    return {
        'sources': sources,
        'topics': topics
    }


def get_academic_config() -> Dict:
    """
    Get academic sources configuration
    """
    config = load_yaml('sources.yaml')
    academic = config.get('academic', {})
    
    arxiv_config = academic.get('arxiv', {})
    categories = arxiv_config.get('categories', ['cs.AI', 'cs.CY'])
    
    logger.info(f"Loaded academic config: {len(categories)} arXiv categories")
    return {
        'categories': categories,
        'arxiv_enabled': arxiv_config.get('enabled', True),
        'ieee_enabled': academic.get('ieee', {}).get('enabled', False)
    }


def get_scraping_config() -> Dict:
    """
    Get complete scraping configuration
    Returns all keywords, sources, and settings
    """
    return {
        'keywords': get_all_keywords(),
        'rss_feeds': get_rss_feeds(),
        'tech_news': get_tech_news_config(),
        'academic': get_academic_config()
    }
