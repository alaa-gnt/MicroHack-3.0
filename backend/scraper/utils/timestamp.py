"""
Timestamp utilities for the scraping system
"""
from datetime import datetime, timezone
from typing import Optional


def now_iso8601() -> str:
    """
    Get current UTC timestamp in ISO 8601 format
    
    Returns:
        ISO 8601 formatted string (e.g., "2026-02-06T10:30:00Z")
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_iso8601_timestamp() -> str:
    """
    Alias for now_iso8601
    """
    return now_iso8601()


def parse_iso8601(date_str: str) -> Optional[datetime]:
    """
    Parse ISO 8601 date string to datetime
    
    Args:
        date_str: ISO 8601 formatted string
    
    Returns:
        datetime object or None if parsing fails
    """
    try:
        # Handle 'Z' suffix
        if date_str.endswith('Z'):
            date_str = date_str[:-1] + '+00:00'
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime to string
    """
    return dt.strftime(fmt)


def get_utc_now() -> datetime:
    """
    Get current UTC datetime
    """
    return datetime.now(timezone.utc)


def timestamp_to_epoch(dt: datetime) -> int:
    """
    Convert datetime to Unix epoch timestamp
    """
    return int(dt.timestamp())


def epoch_to_timestamp(epoch: int) -> datetime:
    """
    Convert Unix epoch timestamp to datetime
    """
    return datetime.fromtimestamp(epoch, tz=timezone.utc)
