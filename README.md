# 🧳 Travel Agent: Smart Trip Extraction, Calendar Sync, and Summary Mailing

**Travel Agent** is an intelligent automation tool that reads your travel-related Gmail emails, extracts trip information using Claude AI, saves the details in a local database, creates Google Calendar events, and sends you a professionally formatted summary via email. It also provides a frontend to browse your trips visually.

---

## 📌 Key Features

- 🔍 **Email Parsing**  
  Automatically scans your Gmail inbox for flights, hotels, train bookings, and reservations.

- 🧠 **AI-Powered Extraction (Claude)**  
  Uses Anthropic's Claude to extract structured trip data (vendor, dates, locations, etc.) from unstructured email content.

- 🗂️ **SQLite Database**  
  Stores all your trips, including origin and destination, with timestamps.

- 📅 **Google Calendar Integration**  
  Instantly creates calendar events for each reservation with reminders.

- 📧 **HTML Email Summary**  
  Sends you a neatly formatted, mobile-friendly table of your travel schedule.

- 🌐 **Flask Frontend UI**  
  View all your saved trips in a beautiful web dashboard (`localhost:5000`).

---

![image_alt](https://github.com/abhinav7289A/Travel_Agent/blob/main/Editor%20_%20Mermaid%20Chart-2025-07-01-060423.png?raw=true)

## 🛠️ Technologies Used

| Component       | Technology                            |
|----------------|----------------------------------------|
| Backend         | Python 3.11                            |
| Web Framework   | Flask                                  |
| Email Access    | Gmail API (OAuth2 via Google API)      |
| Calendar Sync   | Google Calendar API                    |
| AI Extraction   | Claude (Anthropic API)                 |
| Database        | SQLite                                 |
| Frontend        | HTML5, CSS3, Bootstrap                 |
| Environment     | `.env` via `python-dotenv`             |

---

## 📁 Project Structure

```bash
Travel_Agent/
├── app/
│   ├── web_app.py           # Flask web app for displaying trips
│   ├── models.py            # DB logic (init, insert, fetch)
│   ├── gmail_client.py      # Gmail API for fetching emails
│   ├── calendar_client.py   # Google Calendar event creation
│   ├── claude_utils.py      # Trip info extraction using Claude
│   └── templates/
│       └── index.html       # Frontend trip viewer
├── main.py                  # Runs the pipeline end-to-end
├── .env                     # Secrets & configuration
├── credentials.json         # Google API credentials
├── token.json               # Saved access tokens
├── trips.db                 # SQLite database
└── README.md                # You're here!
