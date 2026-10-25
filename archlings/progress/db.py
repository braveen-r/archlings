import duckdb
import os
from datetime import datetime

DB_PATH = "archlings.duckdb"

def init_db():
    with duckdb.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                scenario_id VARCHAR PRIMARY KEY,
                status VARCHAR,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                hints_used INTEGER DEFAULT 0
            )
        """)

def mark_started(scenario_id: str):
    init_db()
    now = datetime.now()
    with duckdb.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO progress (scenario_id, status, start_time, hints_used)
            VALUES (?, 'started', ?, 0)
            ON CONFLICT (scenario_id) DO UPDATE SET 
                status = 'started',
                start_time = ?,
                hints_used = 0
        """, (scenario_id, now, now))

def mark_completed(scenario_id: str):
    now = datetime.now()
    with duckdb.connect(DB_PATH) as conn:
        conn.execute("""
            UPDATE progress 
            SET status = 'completed', end_time = ? 
            WHERE scenario_id = ?
        """, (now, scenario_id))
        
        # Calculate duration in seconds
        result = conn.execute("""
            SELECT date_diff('second', start_time, end_time) as duration, hints_used
            FROM progress WHERE scenario_id = ?
        """, (scenario_id,)).fetchone()
        return result

def get_all_progress():
    init_db()
    with duckdb.connect(DB_PATH) as conn:
        return conn.execute("SELECT scenario_id, status, hints_used FROM progress").fetchall()
