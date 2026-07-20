#!/usr/bin/env python3
"""
US Stock Market News Email Bot (SendGrid Version)
"""

import os
import sys
import requests
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ─── Configuration ───
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", EMAIL_SENDER)

# Validate env vars
missing = []
if not ALPHA_VANTAGE_API_KEY:
    missing.append("ALPHA_VANTAGE_API_KEY")
if not SENDGRID_API_KEY:
    missing.append("SENDGRID_API_KEY")
if not EMAIL_SENDER:
    missing.append("EMAIL_SENDER")
if not EMAIL_RECIPIENT:
    missing.append("EMAIL_RECIPIENT")

if missing:
    print(f"ERROR: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)


def fetch_stock_news():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": "SPY",
        "limit": 5,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "feed" not in data or not data["feed"]:
            return None, "No news available at the moment."

        top_article = data["feed"][0]
        title = top_article.get("title", "No title")
        source = top_article.get("source", "Unknown")
        url_link = top_article.get("url", "")
        summary = top_article.get("summary", "")

        return title, source, url_link, summary

    except requests.exceptions.RequestException as e:
        return None, f"Error fetching news: {e}"


def send_email(subject, body_html, body_text):
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_RECIPIENT,
        subject=subject,
        html_content=body_html,
        plain_text_content=body_text,
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)

    print(f"Email sent! Status code: {response.status_code}")
    print(f"Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def build_email_content(title, source, url_link, summary):
    today = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"📈 US Stock Market News — {today}"

    body_text = f"""US Stock Market News — {today}

Today's Headline:
{title}

Source: {source}
Read more: {url_link}

Summary:
{summary}

—
Sent by your Stock News Bot
"""

    body_html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 20px; font-weight: 600; }}
        .header .date {{ margin-top: 6px; opacity: 0.85; font-size: 14px; }}
        .content {{ padding: 28px; }}
        .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 8px; }}
        .headline {{ font-size: 22px; font-weight: 700; color: #1a1a1a; line-height: 1.4; margin-bottom: 12px; }}
        .meta {{ font-size: 13px; color: #666; margin-bottom: 16px; }}
        .summary {{ font-size: 15px; color: #444; line-height: 1.6; background: #f8f9fa; padding: 16px; border-radius: 8px; border-left: 4px solid #1a73e8; }}
        .cta {{ margin-top: 24px; text-align: center; }}
        .cta a {{ display: inline-block; background: #1a73e8; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-weight: 500; font-size: 14px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #999; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 US Stock Market News</h1>
            <div class="date">{today}</div>
        </div>
        <div class="content">
            <div class="label">Today's Headline</div>
            <div class="headline">{title}</div>
            <div class="meta">Source: {source}</div>
            <div class="summary">{summary}</div>
            <div class="cta">
                <a href="{url_link}" target="_blank">Read Full Article →</a>
            </div>
        </div>
        <div class="footer">
            Sent by your Stock News Bot<br>
            Every weekday at 9:40 AM ET
        </div>
    </div>
</body>
</html>"""

    return subject, body_html, body_text


def main():
    print("Fetching latest US stock market news...")

    result = fetch_stock_news()

    if result[0] is None:
        error_msg = result[1]
        print(f"Error: {error_msg}")
        subject = f"⚠️ Stock News Bot Error — {datetime.now().strftime('%A, %B %d')}"
        body_text = f"Could not fetch news today.\n\nError: {error_msg}"
        body_html = f"<p>Could not fetch news today.</p><p>Error: {error_msg}</p>"
        send_email(subject, body_html, body_text)
        return

    title, source, url_link, summary = result
    print(f"Headline: {title}")

    subject, body_html, body_text = build_email_content(title, source, url_link, summary)
    send_email(subject, body_html, body_text)


if __name__ == "__main__":
    main()
