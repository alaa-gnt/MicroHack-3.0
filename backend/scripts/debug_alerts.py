
import psycopg
from datetime import date
from psycopg.rows import dict_row

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def check_alerts():
    print("🔍 Checking Alerts Data (via psycopg)...")
    try:
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                today = date.today()
                print(f"Checking for date: {today}")

                # 1. Total Alerts
                cur.execute("SELECT count(*) FROM alerts")
                total = cur.fetchone()['count']
                print(f"Total alerts in DB: {total}")

                if total > 0:
                    cur.execute("SELECT created_at FROM alerts LIMIT 1")
                    first_created = cur.fetchone()['created_at']
                    print(f"Sample alert created_at: {first_created} (type: {type(first_created)})")

                # 2. Alerts Today (Logic from analytics.py: func.date(Alert.created_at) == today)
                # In Postgres, equivalent is usually: created_at::date = 'YYYY-MM-DD'
                
                query = "SELECT count(*) FROM alerts WHERE created_at::date = %s"
                cur.execute(query, (today,))
                alerts_today = cur.fetchone()['count']
                print(f"Alerts today (SQL match): {alerts_today}")

                # 3. Breakdown
                query_critical = "SELECT count(*) FROM alerts WHERE created_at::date = %s AND severity IN ('Critical', 'High')"
                cur.execute(query_critical, (today,))
                critical = cur.fetchone()['count']
                print(f"Critical/High alerts today: {critical}")

                query_minor = "SELECT count(*) FROM alerts WHERE created_at::date = %s AND severity IN ('Medium', 'Low')"
                cur.execute(query_minor, (today,))
                minor = cur.fetchone()['count']
                print(f"Medium/Low alerts today: {minor}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_alerts()
