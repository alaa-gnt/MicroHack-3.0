import os
import csv
import json
from dotenv import load_dotenv

load_dotenv()

from workflow import app

def run_pipeline(signals):
    print("🚀 Starting ReAct Multi-Agent Processing...")
    results = []
    
    for i, signal in enumerate(signals, 1):
        sig_id = f"SIG-{i}"
        print(f"\nProcessing {sig_id}...")
        
        # Initializing the state
        initial_state = {
            "signal_id": sig_id,
            "signal_text": signal,
            "corrected_text": "", 
            "domain": "",
            "impact": 0.0,
            "urgency": 0.0,
            "tri": 0.0,
            "technologies": [],
            "companies": [],
            "location": "",
            "retry_count": 0,
            "processing_errors": [],
            "agent_thoughts": []
        }
        
        # Unique thread for LangGraph checkpointer
        config = {"configurable": {"thread_id": f"thread_{sig_id}"}}
        
        try:
            # Running the compiled graph
            final_state = app.invoke(initial_state, config=config)
            results.append(final_state)
            print(f"✅ Success: Tri-Score {final_state.get('tri')}")
        except Exception as e:
            print(f"❌ Error processing {sig_id}: {e}")

    return results

def save_results(results):
    os.makedirs("./data", exist_ok=True)
    
    # 1. Save JSON (Full State Dump)
    with open("./data/processed_signals.json", "w") as f:
        json.dump(results, f, indent=4)
    
    # 2. Save CSV (Clean Spreadsheet View)
    # Added 'corrected_text' to the headers
    keys = [
        "signal_id", 
        "corrected_text", 
        "domain", 
        "impact", 
        "urgency", 
        "tri", 
        "technologies", 
        "companies", 
        "location", 
        "retry_count"
    ]
    
    try:
        with open("./data/processed_signals.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        print("📂 Local CSV/JSON files updated in ./data/")
    except Exception as e:
        print(f"❌ File Save Error: {e}")

if __name__ == "__main__":
    # Add your real hackathon signals here
    test_signals = [
        "IBM announces a new 1000-qubit quantum processor called Condor.",
        "A new IoT sensor system for smart grids in Singapore.",
        "A cybersecurity breach at a major financial institution.",
        "A new AI chip for autonomous vehicles has been developed by NVIDIA.",
        "A new biometric authentication system has been implemented in China.",
        "A new quantum computing breakthrough has been made by Google.",
        "Microsoft explores underwater data centers for sustainable cooling.",
        "Toyota partners with Panasonic for next-gen solid-state batteries.",
        "SpaceX successfully lands Starship booster on launch platform.",
        "Ethereum transitions to Proof of Stake, reducing energy consumption by 99%.",
        "Meta introduces a new AR glass prototype for social interactions.",
        "Amazon launches Project Kuiper satellite to provide global internet.",
        "Apple announces M4 chip with neural engine for AI tasks.",
        "DeepMind's AlphaFold predicts structure of nearly all known proteins.",
        "TSMC starts mass production of 2nm chips in Hsinchu.",
        "OpenAI releases GPT-5 with improved reasoning capabilities.",
        "Tesla's Optimus robot demonstrates autonomous battery swap.",
        "Moderna develops mRNA vaccine for seasonal influenza.",
        "Samsung unveils world's first rollable OLED display phone.",
        "Intel invests $20B in new chip manufacturing sites in Ohio."
    ]
    
    # TEST: Run with limited signals (1 for initial test, 5 for stress test)
    num_signals = 15  # Change to 5 for next test
    processed_data = run_pipeline(test_signals[:num_signals])
    save_results(processed_data)