"""
HTTP client with retry logic and timeout handling
Uses requests library with exponential backoff
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
import time
from utils.logger import setup_logger

logger = setup_logger(__name__)

class HTTPClient:
    """
    Robust HTTP client with retries and timeout
    """
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry strategy
        """
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,  # Wait 1s, 2s, 4s between retries
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers to mimic browser
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        return session
    
    def get(self, url: str, params: Optional[dict] = None, timeout: Optional[int] = None) -> requests.Response:
        """
        GET request with error handling
        """
        try:
            timeout = timeout or self.timeout
            logger.info(f"GET request to: {url}")
            
            response = self.session.get(
                url,
                params=params,
                timeout=timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            logger.info(f"Success: {url} - Status {response.status_code}")
            return response
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error for {url}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            raise
    
    def post(self, url: str, data: Optional[dict] = None, json: Optional[dict] = None) -> requests.Response:
        """
        POST request with error handling
        """
        try:
            logger.info(f"POST request to: {url}")
            
            response = self.session.post(
                url,
                data=data,
                json=json,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Success: {url} - Status {response.status_code}")
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"POST error for {url}: {str(e)}")
            raise
    
    def close(self):
        """Close session"""
        self.session.close()