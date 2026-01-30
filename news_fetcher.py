import requests
import config

def fetch_top_headlines():
    """
    Fetches top headlines from NewsAPI.
    Returns a list of articles or an empty list if failed.
    """
    if not config.NEWS_API_KEY:
        print("Error: NEWS_API_KEY is not set.")
        return []

    params = {
        'apiKey': config.NEWS_API_KEY,
        'country': 'us', # Default to US news
        'category': 'general',
        'pageSize': 20
    }
    
    try:
        response = requests.get(config.NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            return data.get('articles', [])
        else:
            print(f"NewsAPI Error: {data.get('message')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
