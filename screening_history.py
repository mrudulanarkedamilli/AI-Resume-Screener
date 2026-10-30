
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "screening_history.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            job_title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            results_json TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_screening(user_email, job_title, ranking):
    if not user_email:
        raise ValueError("Please sign in first.")

    if ranking.empty:
        raise ValueError("No ranking results to save.")

    records = json.loads(
        ranking.to_json(orient="records")
    )

    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO screenings
            (user_email, job_title, created_at, results_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_email.strip().lower(),
                job_title.strip() or "Untitled Job",
                datetime.now(timezone.utc).isoformat(
                    timespec="seconds"
                ),
                json.dumps(records)
            )
        )
        return cursor.lastrowid


def get_screenings(user_email):
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, job_title, created_at
            FROM screenings
            WHERE user_email = ?
            ORDER BY id DESC
            """,
            (user_email.strip().lower(),)
        ).fetchall()

    return [dict(row) for row in rows]


def load_screening(screening_id, user_email):
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT results_json
            FROM screenings
            WHERE id = ? AND user_email = ?
            """,
            (screening_id, user_email.strip().lower())
        ).fetchone()

    if row is None:
        return None

    return pd.DataFrame(json.loads(row["results_json"]))


def delete_screening(screening_id, user_email):
    with get_db() as conn:
        cursor = conn.execute(
            """
            DELETE FROM screenings
            WHERE id = ? AND user_email = ?
            """,
            (screening_id, user_email.strip().lower())
        )
        return cursor.rowcount > 0
