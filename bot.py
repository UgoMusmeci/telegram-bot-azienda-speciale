import feedparser
import requests
import os

RSS_URL = "https://ugomusmeci.github.io/azienda-speciale-rss/feed.xml"

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = os.getenv("CHAT_ID")

LAST_FILE = "last_news.txt"

print("Leggo feed RSS...")

feed = feedparser.parse(RSS_URL)

if not feed.entries:

    print("Nessuna news trovata")
    exit()

ultima_news = feed.entries[0]

news_id = ultima_news.link

print(f"Ultima news: {ultima_news.title}")

ultima_salvata = ""

if os.path.exists(LAST_FILE):

    with open(
        LAST_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        ultima_salvata = f.read().strip()

if news_id == ultima_salvata:

    print("Nessuna nuova news")
    exit()

descrizione = ultima_news.description

if len(descrizione) > 400:

    descrizione = descrizione[:400] + "..."

messaggio = (
    f"📢 <b>{ultima_news.title}</b>\n\n"
    f"{descrizione}\n\n"
    f"<a href='{ultima_news.link}'>Leggi la notizia</a>"
)

url = (
    f"https://api.telegram.org/"
    f"bot{BOT_TOKEN}/sendMessage"
)

payload = {
    "chat_id": CHAT_ID,
    "text": messaggio,
    "parse_mode": "HTML",
    "disable_web_page_preview": False
}

print("Invio messaggio Telegram...")

response = requests.post(
    url,
    data=payload
)

if response.status_code == 200:

    print("News inviata correttamente")

    with open(
        LAST_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(news_id)

else:

    print("Errore invio Telegram")
    print(response.text)
    exit(1)