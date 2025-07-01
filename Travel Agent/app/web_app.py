import os
import json
from flask import Flask, render_template
from dotenv import load_dotenv

from app.models import init_db, get_all_trips

# Load environment (for RECIPIENT_EMAIL or anything else, if needed)
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    # Ensure DB/table exist
    init_db()

    # Fetch trips; each dict has keys: vendor, reservation_code, start_date,
    # end_date, origin, destination
    trips = get_all_trips()

    # Debug: print the trips so you can see them in console
    print("🛈 Trips passed to template:")
    print(json.dumps(trips, indent=2))

    return render_template("index.html", trips=trips)


if __name__ == "__main__":
    app.run(debug=True)
