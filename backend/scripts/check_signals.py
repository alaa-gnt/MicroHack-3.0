from app.database.postgres import SessionLocal
from app.models.signal import Signal

def check_db():
    db = SessionLocal()
    try:
        count = db.query(Signal).count()
        print(f"\n[DB CHECK] Found {count} signals in the database.")
        
        last_signals = db.query(Signal).order_by(Signal.date.desc()).limit(5).all()
        if last_signals:
            print("\nLast 5 signals:")
            for s in last_signals:
                print(f"- {s.title} (Source: {s.source_name})")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
