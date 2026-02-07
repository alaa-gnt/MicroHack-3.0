from typing import TypedDict, List, Optional, Dict, Any


class RawDocument(TypedDict):
    url: str
    source: str
    title: str
    text: str
    published_date: str


class Signal(TypedDict):
    id: str
    url: str
    source: str
    title: str
    text: str
    scraping_date: str
    is_processed: bool


class GraphState(TypedDict, total=False):
    # Orchestrator output
    action: str                     # "proceed" | "skip"
    sources: List[str]
    keywords: List[str]

    # Scraping
    raw_documents: List[RawDocument]

    # Filtering
    valid_documents: List[RawDocument]

    # Final output
    signals: List[Signal]

    # Metadata
    batch_id: str
