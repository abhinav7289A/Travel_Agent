import os
from googleapiclient.discovery import build
from .gmail_client import get_credentials

def build_calendar_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)

def create_calendar_event(trip: dict):
    """
    Creates a simple all‐day calendar event for the trip.
    Expects trip keys: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD or None), vendor, reservation_code.
    """
    service = build_calendar_service()
    start = trip.get("start_date")
    # Use end_date + 1 day if provided, otherwise same day
    end = trip.get("end_date") or start

    event = {
        "summary": f"{trip.get('vendor', 'Trip')} ({trip.get('reservation_code','')})",
        "start": {"date": start},
        "end":   {"date": end},
        "description": f"Location: {trip.get('location')}",
    }

    created = service.events().insert(calendarId="primary", body=event).execute()
    return created.get("htmlLink")