import time
import schedule
import config
import database
import news_fetcher
import content_processor
import telegram_bot

def job():
    print("Starting news fetch job...")
    articles = news_fetcher.fetch_top_headlines()
    
    if not articles:
        print("No articles fetched.")
        return

    print(f"Fetched {len(articles)} articles.")
    
    for article in articles:
        url = article.get('url')
        title = article.get('title')
        description = article.get('description') or "No description available."
        
        if not url or not title:
            continue

        if database.news_exists(url):
            print(f"Skipping existing news: {title}")
            continue

        print(f"Processing new article: {title}")
        
        # Rewrite/Translate
        my_title, my_summary = content_processor.process_article(title, description, url)
        
        if my_title and my_summary:
            # Send to Telegram
            if telegram_bot.send_news(my_title, my_summary, url):
                # Log to DB only if sent successfully
                database.add_news(url, title)
                print(f"Processed and sent: {title}")
            else:
                print(f"Failed to send: {title}")
        else:
            print(f"Failed to process content for: {title}")

        # Be nice to APIs
        time.sleep(2) 

    print("Job finished.")

def main():
    print("Initializing Database...")
    database.init_db()
    
    # Run once immediately on startup
    job()

    # Schedule
    print(f"Scheduling job every {config.FETCH_INTERVAL_MINUTES} minutes...")
    schedule.every(config.FETCH_INTERVAL_MINUTES).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
