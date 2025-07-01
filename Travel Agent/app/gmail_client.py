import os
import pickle
from pathlib import Path
import base64
from bs4 import BeautifulSoup
from email import message_from_bytes
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

# 1. Which scopes (permissions) we need:
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_credentials():
    """
    1) Looks for a saved token.pickle file.
    2) If missing or invalid, runs the OAuth2 flow to produce one.
    """
    creds = None
    token_path = Path(__file__).parent.parent / "token.pickle"

    # Load existing credentials
    if token_path.exists():
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    # If no valid creds, go through OAuth flow
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            # GOOGLE_CREDENTIALS in .env should point here:
            os.getenv("GOOGLE_CREDENTIALS", "google_creds.json"),
            SCOPES
        )
        # This will open a browser window for you to log in/approve
        creds = flow.run_local_server(port=0)

        # Save for next time
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return creds

def build_gmail_service():
    """Return an authorized Gmail API service client."""
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)

def build_calendar_service():
    """Return an authorized Calendar API service client."""
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)

# app/gmail_client.py (add at the bottom, replacing old get_email_body)



def get_email_body(service, message_id: str) -> str:
    """
    Fetch the raw email, then:
      • Prefer text/plain
      • Fallback to text/html (with tags stripped)
    Returns a UTF-8 string.
    """
    # 1. Fetch raw message
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="raw"
    ).execute()

    raw_data = base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
    email_msg = message_from_bytes(raw_data)

    text_parts = []
    html_parts = []

    # 2. Walk all parts
    if email_msg.is_multipart():
        for part in email_msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))
            # skip attachments
            if ctype == "text/plain" and "attachment" not in disp:
                payload = part.get_payload(decode=True)
                if payload:
                    text_parts.append(payload.decode(part.get_content_charset() or "utf-8", errors="ignore"))
            elif ctype == "text/html" and "attachment" not in disp:
                payload = part.get_payload(decode=True)
                if payload:
                    html_parts.append(payload.decode(part.get_content_charset() or "utf-8", errors="ignore"))
    else:
        # Not multipart – direct payload
        payload = email_msg.get_payload(decode=True)
        if payload:
            text_parts.append(payload.decode(email_msg.get_content_charset() or "utf-8", errors="ignore"))

    # 3. Return plain text if available
    if text_parts:
        return "\n".join(text_parts)

    # 4. Otherwise, clean and return HTML
    if html_parts:
        combined_html = "\n".join(html_parts)
        soup = BeautifulSoup(combined_html, "html.parser")
        return soup.get_text(separator="\n")

    # 5. Fallback empty string
    return ""

def get_label_id(service, label_name: str) -> str:
    """Return the Gmail internal ID for the user label matching label_name."""
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for lbl in labels:
        if lbl["name"].lower() == label_name.lower():
            return lbl["id"]
    raise ValueError(f"Label '{label_name}' not found in your Gmail.")

def send_email(recipient: str, subject: str, html_content: str):
    """
    Sends an HTML email to `recipient` via Gmail API.
    """
    service = build_gmail_service()
    message = MIMEText(html_content, "html")
    message["to"] = recipient
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    try:
        sent = service.users().messages().send(userId="me", body=body).execute()
        return sent
    except HttpError as e:
        print("Failed to send email:", e)
        return None