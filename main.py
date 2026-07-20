import requests
import xml.etree.ElementTree as ET

def get_market_news():
    """
    Fetches the latest business news from Google News RSS and prints it
    as HTML to stdout so it can be captured by the GitHub Action.
    """
    rss_url = "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(rss_url, headers=headers)
        response.raise_for_status()
        
        # Parse the RSS XML feed
        root = ET.fromstring(response.content)
        news_items = root.findall(".//item")[:5]  # Take the top 5 stories
        
        # Build the HTML body
        html_content = "<html><body>"
        html_content += "<h2>Daily Market News Update</h2><ul>"
        
        for item in news_items:
            title = item.find("title").text
            link = item.find("link").text
            html_content += f"<li><a href='{link}'>{title}</a></li>"
            
        html_content += "</ul></body></html>"
        
        # Print to stdout; the GitHub Action workflow will capture this in news_body.txt
        print(html_content)
        
    except Exception as e:
        # Print a simple error message that will be captured in the email if it fails
        print(f"<html><body><p>Error fetching news: {e}</p></body></html>")

if __name__ == "__main__":
    get_market_news()
