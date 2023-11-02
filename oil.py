import requests
import json
import threading
import warnings
import subprocess

from bs4 import BeautifulSoup
from flask import Flask, request
from linebot.models import TextSendMessage
from linebot import LineBotApi, WebhookHandler, LineBotSdkDeprecatedIn30


def check_oil_price(user_id):
    api = LineBotApi(
        "lzAAH48tUDN4ovgVj/O3HAJHwUuBCLjhLc14vuxs7dx7lHytHR7W7JnxZBjnP3udsmyd+3ttHLBYmoBDYoipx7A1xg/gmwqjYCKbbprttaeYq+SqwkuctyLTsrRZvP7f4RduiFwk4PBK0DiFjWRR5QdB04t89/1O/w1cDnyilFU="
    )
    # 目標網址
    url = "https://gas.goodlife.tw/"
    price_array = []
    # 輸出用
    output_keyword = [
        "92汽油",
        "95汽油",
        "98汽油",
    ]
    # 搜尋網站元素關鍵字
    search_keyword = [
        "92:",
        "95油價:",
        "98:",
    ]
    # 目前油價
    output_curr_price = ""
    # 下週調整
    output_oli_price_adjust = ""

    html = requests.get(url)
    # 此網站編碼使用ISO-8859-1需更改編碼為utf-8
    soup = BeautifulSoup(html.content, "html.parser", from_encoding="utf-8")

    # 油價
    for i in search_keyword:
        price = soup.find(lambda tag: tag.name == "li" and i in tag.text)
        price = price.text.split("\n")
        price_array.append(price[2])

    # 下周油價
    data = soup.find("li", class_="main").text.split()

    # 網站可能的變化
    if len(data) == 3:
        output_oli_price_adjust = "從下周一起汽油每公升" + data[2]
    elif data[9] == "不":
        output_oli_price_adjust = "從今日起汽油每公升不調整"
    else:
        output_oli_price_adjust = "自"
        for i in range(1, 10):
            output_oli_price_adjust += data[i]

    # 取得目前油價
    for i in range(3):
        output_curr_price += (
            "目前" + output_keyword[i] + "價格:" + str(price_array[i]) + "\n"
        )

    # 傳送訊息給使用者
    api.push_message(user_id, TextSendMessage(text=output_curr_price))
    api.push_message(user_id, TextSendMessage(text=output_oli_price_adjust))


oil = Flask(__name__)


@oil.route("/", methods=["POST"])
def get_reply():
    handler = WebhookHandler("8c9f8136a7b8ccd89dac2ddbd09f8597")
    body = request.get_data(as_text=True)
    json_data = json.loads(body)

    try:
        signature = request.headers["X-Line-Signature"]
        handler.handle(body, signature)
        user_id = json_data["events"][0]["source"]["userId"]
        text = json_data["events"][0]["message"]["text"]

        if text == "油價":
            check_oil_price(user_id)
    except Exception as e:
        print(e)
    return "OK"


if __name__ == "__main__":
    oil.run()
