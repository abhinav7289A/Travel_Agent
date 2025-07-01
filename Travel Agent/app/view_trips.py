from app.models import init_db, get_all_trips

def display_trips():
    init_db()
    trips = get_all_trips()

    if not trips:
        print("No trips found in the database.")
        return

    print(f"Found {len(trips)} saved trips:\n")
    for idx, trip in enumerate(trips, 1):
        print(f"Trip #{idx}")
        print(f"  Vendor: {trip['vendor']}")
        print(f"  Reservation Code: {trip['reservation_code']}")
        print(f"  Start Date: {trip['start_date']}")
        print(f"  End Date: {trip['end_date']}")
        loc = trip['location']
        if loc:
            print(f"  Location: {loc['from']} → {loc['to']}")
        print("─" * 40)

if __name__ == "__main__":
    display_trips()
