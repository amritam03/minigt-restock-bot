import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.karzanddolls.com/collections/mini-gt"

headers = {"User-Agent": "Mozilla/5.0"}

seen_products = {}

def send_photo(title, status, link, image):

    caption = f"""
🚗 MINI GT Update

{title}
Status: {status}

{link}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={
            "photo": requests.get(image).content
        }
    )


def check_products():

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    products = soup.select(".grid-product")

    for p in products:

        title = p.select_one(".grid-product__title").text.strip()
        link = "https://www.karzanddolls.com" + p.a["href"]

        img = p.select_one("img")["src"]

        if img.startswith("//"):
            img = "https:" + img

        soldout = p.select_one(".grid-product__sold-out")

        status = "OUT OF STOCK" if soldout else "IN STOCK"

        if title not in seen_products:

            seen_products[title] = status

            send_photo(title, status, link, img)

        else:

            if seen_products[title] == "OUT OF STOCK" and status == "IN STOCK":

                send_photo(title, "RESTOCKED 🔥", link, img)

                seen_products[title] = status


check_products()

print("bot running")
