import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.karzanddolls.com/collections/mini-gt"

headers = {
    "User-Agent": "Mozilla/5.0"
}

seen_products = {}

def send_photo(title, status, link, image):

    caption = f"🚗 MINI GT Update\n\n{title}\nStatus: {status}\n\n{link}"

    try:
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
    except Exception as e:
        print("Telegram error:", e)


def check_products():

    print("Checking MINI GT products...")

    try:
        r = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print("Website request failed:", e)
        return

    products = soup.find_all("div", class_="grid-product")

    if not products:
        print("No products found (selector issue)")
        return

    for p in products:

        try:
            title_tag = p.find("div", class_="grid-product__title")

            if not title_tag:
                continue

            title = title_tag.text.strip()

            link_tag = p.find("a")

            if not link_tag:
                continue

            link = "https://www.karzanddolls.com" + link_tag["href"]

            img_tag = p.find("img")

            if not img_tag:
                continue

            img = img_tag["src"]

            if img.startswith("//"):
                img = "https:" + img

            soldout = p.find("span", class_="grid-product__sold-out")

            status = "OUT OF STOCK" if soldout else "IN STOCK"

            if title not in seen_products:

                seen_products[title] = status

                send_photo(title, status, link, img)

            else:

                if seen_products[title] == "OUT OF STOCK" and status == "IN STOCK":

                    send_photo(title, "RESTOCKED 🔥", link, img)

                    seen_products[title] = status

        except Exception as e:
            print("Product parsing error:", e)


print("🚀 MiniGT Bot Started")

while True:

    check_products()

    time.sleep(15)
