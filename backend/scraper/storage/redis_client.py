"""
Redis client for storing scraping state
"""
import redis
from datetime import datetime
from typing import Optional
import json

from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Redis key constants
LAST_SCRAPE_KEY = "scraper:last_scrape_time"


def get_redis_client() -> redis.Redis:
    """
    Get Redis client connection
    """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )


def get_last_scrape_time() -> Optional[datetime]:
    """
    Get the timestamp of the last scrape
    
    Returns:
        datetime of last scrape or None if never scraped
    """
    try:
        client = get_redis_client()
        value = client.get(LAST_SCRAPE_KEY)
        
        if value:
            return datetime.fromisoformat(value)
        return None
        
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {e}. Returning None for last scrape time.")
        return None
    except Exception as e:
        logger.error(f"Error getting last scrape time: {e}")
        return None


def save_last_scrape_time(timestamp: datetime) -> bool:
    """
    Save the timestamp of the current scrape
    
    Args:
        timestamp: datetime to save
    
    Returns:
        True if saved successfully
    """
    try:
        client = get_redis_client()
        client.set(LAST_SCRAPE_KEY, timestamp.isoformat())
        logger.info(f"Saved last scrape time: {timestamp.isoformat()}")
        return True
        
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {e}. Scrape time not saved.")
        return False
    except Exception as e:
        logger.error(f"Error saving last scrape time: {e}")
        return False


def store_batch_metadata(batch_id: str, metadata: dict) -> bool:
    """
    Store batch metadata in Redis
    """
    try:
        client = get_redis_client()
        client.set(f"batch:{batch_id}", json.dumps(metadata), ex=86400 * 7)  # 7 days TTL
        return True
    except Exception as e:
        logger.error(f"Error storing batch metadata: {e}")
        return False


def get_batch_metadata(batch_id: str) -> Optional[dict]:
    """
    Get batch metadata from Redis
    """
    try:
        client = get_redis_client()
        value = client.get(f"batch:{batch_id}")
        return json.loads(value) if value else None
    except Exception as e:
        logger.error(f"Error getting batch metadata: {e}")
        return None
