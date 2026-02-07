"""
Prometheus metrics for scraping engine
"""
from prometheus_client import Counter, Gauge, Summary, start_http_server
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Metrics definitions
DOCUMENTS_SCRAPED = Counter(
    'scraper_documents_total', 
    'Total number of documents scraped',
    ['source', 'status']
)

SCRAPING_LATENCY = Summary(
    'scraper_job_latency_seconds',
    'Time spent running a scraping job',
    ['job_type']
)

LAST_SCRAPE_TIMESTAMP = Gauge(
    'scraper_last_run_timestamp_seconds',
    'Timestamp of the last successful scraping run'
)

SIGNAL_BATCH_SIZE = Summary(
    'scraper_signal_batch_size',
    'Number of signals in a handoff batch'
)


def start_metrics_server(port: int = 8000):
    """
    Start Prometheus metrics server
    """
    try:
        start_http_server(port)
        logger.info(f"Metrics server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")


def record_scraping_result(source: str, count: int, success: bool = True):
    """
    Record results of a scraping operation
    """
    status = "success" if success else "failure"
    DOCUMENTS_SCRAPED.labels(source=source, status=status).inc(count)


def record_batch_handoff(size: int):
    """
    Record batch handoff metrics
    """
    SIGNAL_BATCH_SIZE.observe(size)
    LAST_SCRAPE_TIMESTAMP.set_to_current_time()
