import requests
import config

def send_news(title, summary, link):
    """
    Sends the formatted news message to the Telegram channel.
    """
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHANNEL_ID:
        print("Error: Telegram credentials are not set.")
        return False

    # Format the message
    # Telegram supports HTML or Markdown. We'll use HTML for bolding.
    message = f"<b>{title}</b>\n\n{summary}\n\n<a href='{link}'>Read Original</a>"

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': config.TELEGRAM_CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get('ok'):
            print(f"Successfully sent news: {title}")
            return True
        else:
            print(f"Telegram API Error: {data.get('description')}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error sending to Telegram: {e}")
        return False
