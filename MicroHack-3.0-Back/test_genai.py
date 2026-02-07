import os
import sys
# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

# Add app to path
sys.path.append(os.getcwd())

load_dotenv()

try:
    print(f"Python Executable: {sys.executable}")
    print("Importing langchain_google_genai...")
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("Imported langchain_google_genai")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"GENERAL ERROR: {e}")
    sys.exit(1)

from app.database.postgres import SessionLocal
from app.models.opportunity import Opportunity

def test_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("Missing GOOGLE_API_KEY")
        return

    try:
        print("Testing basic generation...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,
            google_api_key=api_key
        )
        response = llm.invoke("Say 'Hello World'")
        print(f"LLM Response: {response.content}")
        
    except Exception as e:
        print(f"LLM Error: {e}")
        # import traceback
        # traceback.print_exc()

def test_db_access():
    print("\nTesting DB Access...")
    db = SessionLocal()
    opp_id = "c260d870-0c17-4c47-a6b6-efe7c4a2baf3"
    try:
        opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if opp:
            print(f"Found Opportunity: {opp.signal.title if opp.signal else 'No Title'}")
        else:
            print(f"Opportunity {opp_id} not found")
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_genai()
    test_db_access()
