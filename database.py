import sqlite3
import config

def get_db_connection():
    conn = sqlite3.connect(config.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sent_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def news_exists(url):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM sent_news WHERE url = ?', (url,))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_news(url, title):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO sent_news (url, title) VALUES (?, ?)', (url, title))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already exists
    finally:
        conn.close()
