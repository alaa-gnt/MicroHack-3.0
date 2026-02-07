import psycopg

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def update_schema():
    print("🛠️ Updating database schema...")
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                # Add corrected_text column if it doesn't exist
                cur.execute("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                                       WHERE TABLE_NAME='signal_analysis_opportunity' 
                                       AND COLUMN_NAME='corrected_text') THEN
                            ALTER TABLE signal_analysis_opportunity ADD COLUMN corrected_text TEXT;
                            RAISE NOTICE 'Column corrected_text added to signal_analysis_opportunity';
                        ELSE
                            RAISE NOTICE 'Column corrected_text already exists';
                        END IF;
                    END $$;
                """)
                print("✅ Schema update complete.")
    except Exception as e:
        print(f"❌ Schema update failed: {e}")

if __name__ == "__main__":
    update_schema()
