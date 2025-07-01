import os
import json
from dotenv import load_dotenv

from app.gmail_client import build_gmail_service, get_email_body, send_email
from app.models import init_db, save_trip, get_all_trips
from app.claude_utils import extract_trip_details_via_claude
from app.calendar_client import create_calendar_event

# Load environment variables
load_dotenv()
USER_EMAIL = os.getenv("RECIPIENT_EMAIL")

def main():
    # 1) Initialize DB
    init_db()

    # 2) Gmail client
    service = build_gmail_service()

    # 3) Query
    query = os.getenv(
        "GMAIL_QUERY",
        "subject:(flight OR reservation OR itinerary OR booking)"
    )

    # 4) Fetch messages
    msgs = service.users().messages().list(
        userId="me", q=query, maxResults=5
    ).execute().get("messages", [])

    if not msgs:
        print(f"No messages for query: {query}")
        return

    print(f"Fetched {len(msgs)} messages\n")

    # 5) Process each email
    for m in msgs:
        msg_id = m["id"]
        body = get_email_body(service, msg_id)
        print("─"*50)
        print(body[:200].replace("\r\n","\n"), "…\n")

        print("Extracting via Claude…")
        trip = extract_trip_details_via_claude(body)
        print("Parsed trip:", trip)

        save_trip(trip)
        print("✔ Saved trip")

        link = create_calendar_event(trip)
        print("↳ Calendar event created:", link, "\n")

    # 6) Build HTML summary using origin/destination
    rows = []
    for t in get_all_trips():
        rows.append(f"""
            <tr>
                <td>{t['vendor'] or '-'}</td>
                <td>{t['reservation_code'] or '-'}</td>
                <td>{t['start_date'] or '-'}</td>
                <td>{t['end_date'] or '-'}</td>
                <td>{t['origin'] or '-'}</td>
                <td>{t['destination'] or '-'}</td>
            </tr>
        """)

    html = f"""
    <h2>Travel Itinerary Summary</h2>
    <table border="1" cellpadding="4" cellspacing="0">
      <thead>
        <tr>
          <th>Vendor</th><th>Code</th><th>Start</th><th>End</th><th>From</th><th>To</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
    """

    # 7) Send summary
    sent = False
    if USER_EMAIL:
        res = send_email(USER_EMAIL, "Your Travel Itinerary Summary", html)
        sent = True if res else False

    print("✔ Summary email " + ("sent" if sent else "skipped"))

if __name__ == "__main__":
    main()
