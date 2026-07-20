import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
import requests

def fetch_news():
    # Use the new API key from your GitHub secrets
    api_key = os.getenv("FINNHUB_API_KEY", "").strip()
    # Fetching news for a symbol (e.g., AAPL)
    symbol = "AAPL" 
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2026-07-19&to=2026-07-20&token={api_key}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Failed to fetch news. Status: {response.status_code}"
        
    data = response.json()
    if data and isinstance(data, list):
        # Returns the headline of the first article
        return data[0].get("headline", "No news found.")
    return "No market news today."

# ... rest of your email sending logic
def send_email():
    title = fetch_news()
    # .strip() added to all env variables to prevent header errors
    sender = os.getenv("EMAIL_SENDER", "").strip()
    recipient = os.getenv("EMAIL_RECIPIENT", "").strip()
    
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject='Daily Market Update',
        html_content=f'<strong>Today\'s Headline:</strong><br>{title}'
    )
    
    try:
        # .strip() added to API key
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY", "").strip())
        response = sg.send(message)
        print(f"Status Code: {response.status_code}")
    except Exception as e:
        print(f"Full Error Details: {e}")

if __name__ == "__main__":
    send_email()
