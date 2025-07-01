import os
import anthropic
import json

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def extract_trip_details_via_claude(email_text: str) -> dict:
    prompt = f"""
    You are a travel assistant. Extract the following details from the email below:
    - Vendor (e.g., IndiGo, IRCTC)
    - Reservation Code or PNR (if available)
    - Start Date of the trip
    - End Date (if round trip, else leave as null)
    - Location details in 'from' and 'to' format (e.g., Mumbai to Delhi)

    Only return a JSON object in the following format, with keys exactly as below:
    {{
    "vendor": "...",
    "reservation_code": "...",
    "start_date": "...",
    "end_date": null,
    "location": {{"from": "...", "to": "..."}}
    }}

    Email:
    {email_text}
    """


    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Or use "claude-3-haiku" if you want cheaper/faster inference
        max_tokens=1024,
        temperature=0.2,
        system="You are a helpful assistant that extracts travel data from emails.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text_response = response.content[0].text.strip()

    

    try:
        trip_info = json.loads(text_response)
    except json.JSONDecodeError as e:
        print("JSON parsing error from Claude:", e)
        trip_info = {}


    return trip_info
