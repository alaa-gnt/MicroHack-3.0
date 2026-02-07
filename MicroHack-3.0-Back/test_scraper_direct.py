import sys
import os
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal
from app.services.pipeline_service import PipelineService
import logging

# Set up logging to console to see what's happening
logging.basicConfig(level=logging.INFO)

def test_scraper():
    db = SessionLocal()
    try:
        print("Starting scraping pipeline directly...")
        # Use defaults from YAML for better results
        result = PipelineService.run_scraping_pipeline(
            db=db, 
            keywords=None, 
            sources=None 
        )
        print("\nPipeline Execution Finished.")
        
        if result:
            print(f"\nFinal State Keys: {result.keys()}")
            if "raw_documents" in result:
                print(f"Total Raw Documents: {len(result['raw_documents'])}")
            if "valid_documents" in result:
                print(f"Total Valid Documents: {len(result['valid_documents'])}")
            if "signals" in result:
                print(f"Total Signals: {len(result['signals'])}")
        else:
            print("Pipeline returned no result state.")
        
        # Check DB count immediately after
        from app.models.signal import Signal
        count = db.query(Signal).count()
        print(f"\n[DB CHECK] Found {count} signals in the database.")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_scraper()
