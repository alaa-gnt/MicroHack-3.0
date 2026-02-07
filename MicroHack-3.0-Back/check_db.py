import psycopg
from psycopg.rows import dict_row

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def check_db():
    print("🔍 Checking Database Content...")
    try:
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # 1. Signals Table
                cur.execute("SELECT count(*) FROM signals")
                signals_count = cur.fetchone()['count']
                print(f"\n📊 Signals Table: {signals_count} rows")
                
                if signals_count > 0:
                    cur.execute("SELECT title, is_processed FROM signals LIMIT 5")
                    print("   Latest Signals:")
                    for row in cur.fetchall():
                        status = "✅ Processed" if row['is_processed'] else "⏳ Pending"
                        print(f"   - {row['title'][:70]}... [{status}]")

                # 2. Opportunities Table
                cur.execute("SELECT count(*) FROM signal_analysis_opportunity")
                opp_count = cur.fetchone()['count']
                print(f"\n📊 Analysis Opportunities: {opp_count} rows")
                
                if opp_count > 0:
                    cur.execute("SELECT id, primary_domain, urgency_score, impact_score FROM signal_analysis_opportunity LIMIT 5")
                    print("   Latest Analysis Results:")
                    for row in cur.fetchall():
                        print(f"   - ID: {row['id']} | Domain: {row['primary_domain']} | Urgency: {row['urgency_score']} | Impact: {row['impact_score']}")

                # 3. Feasibility Studies
                cur.execute("SELECT count(*) FROM feasibility_studies")
                feas_count = cur.fetchone()['count']
                print(f"\n📊 Feasibility Studies: {feas_count} rows")
                
                if feas_count > 0:
                    cur.execute("SELECT opportunity_id, overall_feasibility, final_recommendation FROM feasibility_studies LIMIT 5")
                    print("   Latest Studies:")
                    for row in cur.fetchall():
                        print(f"   - OppID: {row['opportunity_id']} | Status: {row['overall_feasibility']}")

                # 4. Linkage Check
                print("\n🔗 Linkage Check:")
                cur.execute("""
                    SELECT count(fs.id) as linked_count 
                    FROM feasibility_studies fs
                    JOIN signal_analysis_opportunity sao ON fs.opportunity_id = sao.id
                """)
                linked = cur.fetchone()['linked_count']
                print(f"   Feasibility Studies linked to Opportunities: {linked}")

                if linked == 0 and feas_count > 0:
                    print("   ⚠️ WARNING: Feasibility studies exist but are NOT linked to Opportunities!")
                    cur.execute("SELECT opportunity_id FROM feasibility_studies LIMIT 1")
                    fs_opp_id = cur.fetchone()['opportunity_id']
                    print(f"   Example FS Opportunity ID: {fs_opp_id}")
                    cur.execute("SELECT id FROM signal_analysis_opportunity LIMIT 1")
                    sao_id = cur.fetchone()['id']
                    print(f"   Example SAO ID: {sao_id}")

    except Exception as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == "__main__":
    check_db()
