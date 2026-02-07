"""
RabbitMQ client for publishing signals to Graph 2
"""
import json
import pika
from typing import Optional

from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


def get_connection() -> Optional[pika.BlockingConnection]:
    """
    Get RabbitMQ connection
    """
    try:
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError as e:
        logger.warning(f"RabbitMQ connection failed: {e}")
        return None


def publish_batch(batch_data: dict) -> bool:
    """
    Publish batch of signals to RabbitMQ
    
    Args:
        batch_data: Dictionary containing:
            - batch_id: str
            - signals_count: int
            - signals: List of signal dicts
    
    Returns:
        True if published successfully
    """
    try:
        connection = get_connection()
        
        if not connection:
            logger.warning("RabbitMQ not available. Batch not published.")
            # For testing: print to console instead
            logger.info(f"[DRY RUN] Would publish batch: {batch_data.get('batch_id')} with {batch_data.get('signals_count')} signals")
            return False
        
        channel = connection.channel()
        
        # Declare queue (creates if doesn't exist)
        channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)
        
        # Publish message
        channel.basic_publish(
            exchange='',
            routing_key=settings.RABBITMQ_QUEUE,
            body=json.dumps(batch_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        
        connection.close()
        
        logger.info(f"Published batch {batch_data.get('batch_id')} to RabbitMQ")
        return True
        
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")
        return False


def publish_signal(signal: dict) -> bool:
    """
    Publish a single signal to RabbitMQ
    """
    return publish_batch({
        'batch_id': signal.get('id', 'single'),
        'signals_count': 1,
        'signals': [signal]
    })
