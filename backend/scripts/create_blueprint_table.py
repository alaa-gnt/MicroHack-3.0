import psycopg

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def update_schema():
    print("🛠️ Creating Venture Blueprints Table...")
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                # Create venture_blueprints table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS venture_blueprints (
                        id VARCHAR PRIMARY KEY,
                        opportunity_id VARCHAR NOT NULL UNIQUE REFERENCES signal_analysis_opportunity(id),
                        system_architecture TEXT,
                        data_schema TEXT,
                        security_protocols TEXT,
                        kpi_metrics TEXT,
                        v0_prompt TEXT,
                        github_manifest JSONB,
                        mermaid_flow TEXT
                    );
                """)
                print("✅ Table venture_blueprints created successfully.")
    except Exception as e:
        print(f"❌ Schema update failed: {e}")

if __name__ == "__main__":
    update_schema()
