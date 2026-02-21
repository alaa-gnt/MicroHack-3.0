import os
import subprocess

def get_db_content():
    # Get table names
    cmd_tables = 'docker exec microhack_db psql -U postgres -d microhack -t -c "SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\';"'
    result = subprocess.run(cmd_tables, shell=True, capture_output=True, text=True)
    tables = [t.strip() for t in result.stdout.split('\n') if t.strip()]
    
    for table in tables:
        print(f"\n{'='*20} TABLE: {table} {'='*20}")
        cmd_content = f'docker exec microhack_db psql -U postgres -d microhack -c "SELECT * FROM {table} LIMIT 10;"'
        subprocess.run(cmd_content, shell=True)

if __name__ == "__main__":
    get_db_content()
