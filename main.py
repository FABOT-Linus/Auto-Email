import os
import requests
import xml.etree.ElementTree as ET
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def get_market_news():
    # Google News RSS for Business/Finance - No API key needed!
    rss_url = "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en"
    
    # Adding a User-Agent header helps prevent the GitHub Actions runner from being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(rss_url, headers=headers)
    response.raise_for_status()
    
    # Parse the XML RSS feed
    root = ET.fromstring(response.content)
    news_items = root.findall(".//item")[:5]  # Grab the top 5 news stories
    
    html_content = "<h2>Daily Market News</h2><ul>"
    for item in news_items:
        title = item.find("title").text
        link = item.find("link").text
        html_content += f"<li><a href='{link}'>{title}</a></li>"
    html_content += "</ul>"
    
    return html_content

def send_email(html_content):
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    message = Mail(
        from_email=os.environ.get('EMAIL_SENDER'),
        to_emails=os.environ.get('EMAIL_RECIPIENT'),
        subject="Your Daily Market Update",
        html_content=html_content
    )
    
    try:
        response = sg.send(message)
        print(f"Email sent successfully! Status Code: {response.status_code}")
    except Exception as e:
        # The 'e' object from SendGrid often contains the specific rejection reason
        print(f"Detailed Error: {e}")
        if hasattr(e, 'body'):
            print(f"Response Body: {e.body}")
