"""
Test individual scrapers
"""
from scrapers.tools.patent_scraper import PatentScraperTool
from scrapers.tools.rss_scraper import RSSScraperTool

def main():
    print("Testing Patent Scraper...")
    patent_tool = PatentScraperTool()
    patents = patent_tool.scrape(keywords=["IoT"], days_back=7)
    print(f"Found {len(patents)} patents")
    
    print("\nTesting RSS Scraper...")
    rss_tool = RSSScraperTool()
    articles = rss_tool.scrape(
        feed_urls=["https://www.porttechnology.org/feed/"],
        days_back=7
    )
    print(f"Found {len(articles)} articles")

if __name__ == "__main__":
    main()