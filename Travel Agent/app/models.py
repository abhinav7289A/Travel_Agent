import os
import sqlite3
import json

# Absolute path to the SQLite database file (one level up from this file)
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "..", "trips.db")

def init_db():
    """
    Initialize the SQLite database and create the 'trips' table if it doesn’t exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            reservation_code TEXT,
            start_date TEXT,
            end_date TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_trip(trip: dict):
    """
    Save a single trip record to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Serialize location dict to JSON string
    loc = trip.get("location")
    if isinstance(loc, dict):
        loc = json.dumps(loc)

    c.execute(
        """
        INSERT INTO trips (vendor, reservation_code, start_date, end_date, location)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trip.get("vendor"),
            trip.get("reservation_code"),
            trip.get("start_date"),
            trip.get("end_date"),
            loc,
        )
    )
    conn.commit()
    conn.close()

def get_all_trips():
    """
    Fetch all saved trips, parse the location JSON, and return a list of dicts
    with separate 'origin' and 'destination' keys.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT vendor, reservation_code, start_date, end_date, location FROM trips")
    rows = c.fetchall()
    conn.close()

    trips = []
    for vendor, code, start, end, loc_str in rows:
        # Parse location JSON into dict
        try:
            loc = json.loads(loc_str) if loc_str else {}
        except json.JSONDecodeError:
            loc = {}

        origin = loc.get("from", "") or ""
        destination = loc.get("to", "") or ""

        trips.append({
            "vendor": vendor,
            "reservation_code": code,
            "start_date": start,
            "end_date": end,
            "origin": origin,
            "destination": destination,
        })

    return trips
