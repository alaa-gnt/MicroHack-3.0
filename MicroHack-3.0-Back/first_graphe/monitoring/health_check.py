"""
Health check logic for core infrastructure dependencies
"""
from typing import Dict, Tuple
from storage.redis_client import get_redis_client
from storage.rabbitmq_client import get_connection
from storage.s3_client import s3_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


def check_redis() -> Tuple[bool, str]:
    """Check Redis connectivity"""
    try:
        client = get_redis_client()
        if client.ping():
            return True, "Redis is healthy"
        return False, "Redis ping failed"
    except Exception as e:
        return False, f"Redis error: {e}"


def check_rabbitmq() -> Tuple[bool, str]:
    """Check RabbitMQ connectivity"""
    try:
        connection = get_connection()
        if connection and connection.is_open:
            connection.close()
            return True, "RabbitMQ is healthy"
        return False, "RabbitMQ connection failed"
    except Exception as e:
        return False, f"RabbitMQ error: {e}"


def check_minio() -> Tuple[bool, str]:
    """Check MinIO connectivity"""
    if not s3_client.client:
        return False, "MinIO client not initialized"
    try:
        if s3_client.client.bucket_exists(s3_client.bucket_name):
            return True, "MinIO is healthy"
        return False, f"MinIO bucket '{s3_client.bucket_name}' not found"
    except Exception as e:
        return False, f"MinIO error: {e}"


def run_all_health_checks() -> Dict[str, Dict]:
    """
    Run all system health checks
    """
    results = {
        "redis": check_redis(),
        "rabbitmq": check_rabbitmq(),
        "minio": check_minio()
    }
    
    overall_healthy = all(r[0] for r in results.values())
    
    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "checks": {name: {"healthy": r[0], "message": r[1]} for name, r in results.items()}
    }
