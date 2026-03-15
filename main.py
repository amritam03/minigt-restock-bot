import requests
from bs4 import BeautifulSoup
import time
import json

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

URL = "https://www.karzanddolls.com/collections/mini-gt"

headers = {
    "User-Agent": "Mozilla/5.0"
}

seen_products = set()

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def check():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    products = soup.select(".grid-product")

    for p in products:

        title = p.select_one(".grid-product__title").text.strip()
        link = "https://www.karzanddolls.com" + p.a["href"]

        sold = p.select_one(".grid-product__sold-out")

        status = "OUT" if sold else "IN STOCK"

        if title not in seen_products:

            seen_products.add(title)

            send(
                f"🆕 MINI GT FOUND\n\n"
                f"{title}\n"
                f"Status: {status}\n"
                f"{link}"
            )

while True:
    try:
        check()
        time.sleep(30)
    except:
        time.sleep(30)
