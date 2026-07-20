import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def fetch_news():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=SPY&limit=1&apikey={api_key}"
    
    # Adding a header to identify the request
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    
    # Check if the status is not 200 (OK)
    if response.status_code != 200:
        print(f"Fetch failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return "Failed to fetch news."
        
    data = response.json()
    return data.get("feed", [{}])[0].get("title", "No market news today.")
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
