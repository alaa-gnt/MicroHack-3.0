"""
LIVE SCRAPING TEST - Runs REAL scrapers and shows REAL signals
This script fetches actual data from live web sources
"""
import sys
import os
import json
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(step_num, title):
    print(f"\n[STEP {step_num}] {title}")
    print("-" * 50)


def run_live_scraping():
    """
    Run REAL scrapers and show REAL signals
    This fetches actual data from the internet!
    """
    print_header("LIVE SCRAPING TEST - REAL DATA FROM WEB")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    all_documents = []
    
    # Check for previous results to detect "new" content
    previous_urls = set()
    data_dir = os.path.join(project_root, "data")
    if os.path.exists(data_dir):
        json_files = [f for f in os.listdir(data_dir) if f.startswith("scraping_results_") and f.endswith(".json")]
        if json_files:
            latest_file = os.path.join(data_dir, sorted(json_files)[-1])
            try:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    prev_data = json.load(f)
                    for signal in prev_data.get('signals', []):
                        previous_urls.add(signal.get('url'))
                print(f"  [INFO] Loaded {len(previous_urls)} URLs from previous run for comparison")
            except Exception:
                pass

    # ===== STEP 1: Patent Scraper =====
    print_step(1, "PATENT SCRAPER - Fetching from Google Patents")
    
    from scrapers.tools.patent_scraper import PatentScraperTool
    from config.loader import get_all_keywords
    
    all_keywords = get_all_keywords()
    keywords = all_keywords[:3]  # Just 3 keywords for speed
    print(f"  Keywords: {keywords}")
    
    patent_scraper = PatentScraperTool()
    # Note: Google Patents is slow, so we limit keywords
    patent_docs = patent_scraper.scrape(keywords=keywords, days_back=30)
    all_documents.extend(patent_docs)
    
    print(f"\n  ✓ Patent Scraper found: {len(patent_docs)} patents")
    if patent_docs:
        new_patents = [d for d in patent_docs if d['url'] not in previous_urls]
        print(f"    - New patents: {len(new_patents)} / {len(patent_docs)}")
        print(f"    Sample: {patent_docs[0]['title'][:60]}...")
    
    # ===== STEP 2: RSS Scraper =====
    print_step(2, "RSS SCRAPER - Fetching real RSS feeds")
    
    from scrapers.tools.rss_scraper import RSSScraperTool
    from config.loader import get_rss_feeds
    
    rss_feeds = get_rss_feeds()
    print(f"  Feeds to scrape: {len(rss_feeds)}")
    
    rss_scraper = RSSScraperTool()
    rss_docs = rss_scraper.scrape(feed_urls=rss_feeds, days_back=7)
    all_documents.extend(rss_docs)
    
    print(f"\n  ✓ RSS Scraper found: {len(rss_docs)} articles")
    if rss_docs:
        new_articles = [d for d in rss_docs if d['url'] not in previous_urls]
        print(f"    - New articles: {len(new_articles)} / {len(rss_docs)}")
        print(f"    Sample: {rss_docs[0]['title'][:60]}...")
    
    # ===== STEP 3: Academic Scraper =====
    print_step(3, "ACADEMIC SCRAPER - Fetching from arXiv API")
    
    from scrapers.tools.academic_scraper import AcademicScraperTool
    
    academic_scraper = AcademicScraperTool()
    # Use different keywords for academic to get more variety
    academic_keywords = all_keywords[3:6] if len(all_keywords) > 5 else keywords
    academic_docs = academic_scraper.scrape(keywords=academic_keywords, days_back=30)
    all_documents.extend(academic_docs)
    
    print(f"\n  ✓ Academic Scraper found: {len(academic_docs)} papers")
    if academic_docs:
        new_papers = [d for d in academic_docs if d['url'] not in previous_urls]
        print(f"    - New papers: {len(new_papers)} / {len(academic_docs)}")
        print(f"    Sample: {academic_docs[0]['title'][:60]}...")
    
    # ===== STEP 4: Tech News Scraper =====
    print_step(4, "TECH NEWS SCRAPER - Fetching from TechCrunch, VentureBeat")
    
    from scrapers.tools.tech_news_scraper import TechNewsScraperTool
    
    tech_scraper = TechNewsScraperTool()
    tech_docs = tech_scraper.scrape(sources=['techcrunch', 'venturebeat'], days_back=7)
    all_documents.extend(tech_docs)
    
    print(f"\n  ✓ Tech News Scraper found: {len(tech_docs)} articles")
    if tech_docs:
        new_tech = [d for d in tech_docs if d['url'] not in previous_urls]
        print(f"    - New articles: {len(new_tech)} / {len(tech_docs)}")
        print(f"    Sample: {tech_docs[0]['title'][:60]}...")
    
    # ===== STEP 5: Quality Filter =====
    print_step(5, "QUALITY FILTER - Filtering valid documents")
    
    from graph.nodes.quality_filter_node import quality_filter_node
    
    filter_result = quality_filter_node({"raw_documents": all_documents})
    valid_docs = filter_result["valid_documents"]
    
    print(f"  Input:  {len(all_documents)} raw documents")
    print(f"  Output: {len(valid_docs)} valid documents")
    print(f"  Filtered: {len(all_documents) - len(valid_docs)}")
    
    # ===== STEP 6: Formatter =====
    print_step(6, "FORMATTER - Converting to Signal format")
    
    from graph.nodes.formatter_node import formatter_node
    
    formatter_result = formatter_node({"valid_documents": valid_docs})
    signals = formatter_result["signals"]
    
    print(f"  Generated: {len(signals)} signals")
    
    # ===== FINAL OUTPUT & STORAGE =====
    print_header("FINAL OUTPUT: REAL SIGNALS")
    
    import uuid
    batch_id = f"batch_{uuid.uuid4().hex[:16]}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output = {
        "batch_id": batch_id,
        "timestamp": datetime.now().isoformat(),
        "signals_count": len(signals),
        "new_signals_count": len([s for s in signals if s['url'] not in previous_urls]),
        "sources_breakdown": {
            "patents": len(patent_docs),
            "rss": len(rss_docs),
            "academic": len(academic_docs),
            "tech_news": len(tech_docs)
        },
        "signals": signals
    }
    
    # Save to JSON file as requested
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    json_path = os.path.join(data_dir, f"scraping_results_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"  [SUCCESS] Results saved to: {os.path.relpath(json_path, project_root)}")
    
    # Print sample of signals instead of full JSON to keep console readable
    if signals:
        print("\n  Sample Signal (First one):")
        sample = signals[0].copy()
        if len(sample.get('text', '')) > 200:
            sample['text'] = sample['text'][:200] + "..."
        print(json.dumps(sample, indent=2, ensure_ascii=False))
    
    print_header("SCRAPING COMPLETE")
    print(f"  Batch ID: {batch_id}")
    print(f"  Total Signals: {len(signals)}")
    print(f"  New Signals: {output['new_signals_count']}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return output


if __name__ == "__main__":
    print("\n🚀 Starting LIVE scraping test...")
    print("   This will fetch REAL data from the internet!")
    print()
    
    try:
        result = run_live_scraping()
    except KeyboardInterrupt:
        print("\n\n❌ Scraping cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
