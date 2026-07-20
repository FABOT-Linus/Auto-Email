import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def fetch_news():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=SPY&limit=1&apikey={api_key}"
    response = requests.get(url).json()
    return response.get("feed", [{}])[0].get("title", "No market news today.")

def send_email():
    title = fetch_news()
    message = Mail(
        from_email=os.getenv("EMAIL_SENDER"),
        to_emails=os.getenv("EMAIL_RECIPIENT"),
        subject='Daily Market Update',
        html_content=f'<strong>Today\'s Headline:</strong><br>{title}'
    )
    
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_email()
