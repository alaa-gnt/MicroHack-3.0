"""
MinIO/S3 client for persisting raw scraping data
"""
import io
import json
from datetime import datetime
from typing import Dict, Any, Optional
from minio import Minio
from minio.error import S3Error

from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class S3Client:
    """
    Client for interacting with MinIO/S3 storage
    """
    
    def __init__(self):
        try:
            self.client = Minio(
                settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            self.bucket_name = settings.MINIO_BUCKET
            self._ensure_bucket()
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}")
            self.client = None

    def _ensure_bucket(self):
        """Ensure the bucket exists, create if not"""
        if not self.client:
            return
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")

    def upload_document(self, doc_id: str, data: Dict[str, Any]) -> bool:
        """
        Upload a document as JSON to S3
        """
        if not self.client:
            logger.warning("MinIO client not available. Upload skipped.")
            return False
            
        try:
            content = json.dumps(data).encode('utf-8')
            content_stream = io.BytesIO(content)
            
            # Generate path: source/year/month/day/id.json
            now = datetime.utcnow()
            source = data.get('source', 'unknown').lower().replace(' ', '_')
            object_name = f"{source}/{now.year}/{now.month:02d}/{now.day:02d}/{doc_id}.json"
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                content_stream,
                length=len(content),
                content_type='application/json'
            )
            
            logger.debug(f"Uploaded document to S3: {object_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload document to S3: {e}")
            return False

    def get_document(self, object_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document from S3
        """
        if not self.client:
            return None
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to retrieve document from S3: {e}")
            return None

# Singleton instance
s3_client = S3Client()
