"""
UUID generation utilities
"""
import uuid
from typing import Optional


def generate_uuid() -> str:
    """
    Generate a new UUID v4
    
    Returns:
        UUID string (e.g., "550e8400-e29b-41d4-a716-446655440000")
    """
    return str(uuid.uuid4())


def generate_short_uuid() -> str:
    """
    Generate a short UUID (first 8 characters)
    
    Returns:
        Short UUID string
    """
    return uuid.uuid4().hex[:8]


def generate_batch_id() -> str:
    """
    Generate a batch ID with prefix
    
    Returns:
        Batch ID (e.g., "batch_550e8400e29b41d4")
    """
    return f"batch_{uuid.uuid4().hex[:16]}"


def is_valid_uuid(uuid_str: Optional[str]) -> bool:
    """
    Validate if string is a valid UUID
    
    Args:
        uuid_str: String to validate
    
    Returns:
        True if valid UUID, False otherwise
    """
    if not uuid_str or not isinstance(uuid_str, str):
        return False
    
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False
