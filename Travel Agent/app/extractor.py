import os
import json
import re
from anthropic import Client

# Initialize the Claude client using your API key
claude = Client(api_key=os.getenv("CLAUDE_API_KEY"))

def extract_itinerary_fields(email_text: str) -> dict:
    """
    Uses Claude (Messages API) to extract itinerary info from the email body.
    """
    system_prompt = (
        "You are a helpful assistant that extracts structured travel itinerary details "
        "from raw email text. Return only a JSON with the keys: "
        "`vendor`, `reservation_code`, `start_date`, `end_date`, `location`.\n"
        "Dates must be in YYYY-MM-DD format. Use null if a field is missing."
    )

    response = claude.messages.create(
        model="claude-3-haiku-20240307",  # fallback Claude 3.5 not supported here
        max_tokens=500,
        temperature=0,
        system=system_prompt,
        messages=[
            {"role": "user", "content": email_text}
        ]
    )

    reply = response.content[0].text.strip()

    # Try parsing JSON
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        # Try extracting JSON from fenced code
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", reply, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        raise ValueError(f"Claude response not valid JSON:\n{reply}")
