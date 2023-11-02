import requests
import json
import warnings
import threading
from bs4 import BeautifulSoup
from datetime import date, datetime, timezone, timedelta
from flask import Flask, request
from linebot.models import TextSendMessage, ImageSendMessage
from linebot import LineBotApi, WebhookHandler, LineBotSdkDeprecatedIn30

import oil  # 油價
import image  # 圖庫


# 天氣
def get_weather_info(location):
    # 修正"台"與"臺"用字
    if location[0] == "台":
        location = "臺" + location[1:]
    # 固定時間格式，timedelta是固定我們的時區
    time_now = (
        datetime.now(tz=timezone(timedelta(hours=8))).strftime("%Y-%m-%d") + "T00:00:00"
    )

    url = (
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-59CC3E4C-89C3-4E32-92C9-02B929228A6A&locationName=&elementName=WeatherDescription&sort=time&timeFrom="
        + time_now
    )
    # 根據api回傳的結果做處理
    response = requests.get(url).json()["records"]["locations"][0]["location"]

    city_list = [
        "新竹縣",
        "金門縣",
        "苗栗縣",
        "新北市",
        "宜蘭縣",
        "雲林縣",
        "臺南市",
        "高雄市",
        "彰化縣",
        "臺北市",
        "南投縣",
        "澎湖縣",
        "基隆市",
        "桃園市",
        "花蓮縣",
        "連江縣",
        "臺東縣",
        "嘉義市",
        "嘉義縣",
        "屏東縣",
        "臺中市",
        "新竹市",
    ]
    # 輸出字串
    return_output = location + "天氣:\n"

    # 確認輸入資料是否正確
    try:
        city_list.index(location)
    except ValueError:
        return ValueError

    # 存放一週的天氣預報資料
    store_data = {}

    # 取得當天的時間資訊
    for i in range(len(response)):
        if response[i]["locationName"] == location:
            response = response[i]["weatherElement"][0]["time"]
            break

    # 取得當天的天氣預報資訊
    for i in range(0, len(response), 2):
        start_time = response[i]["startTime"].split(" ")[0]
        store_data[start_time] = response[i]["elementValue"][0]["value"]

    # 將儲存的資料放入輸出字串
    for i in store_data:
        return_output += i + ":\n " + store_data[i] + "\n"

    return return_output


app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_reply():
    api = LineBotApi(
        "lzAAH48tUDN4ovgVj/O3HAJHwUuBCLjhLc14vuxs7dx7lHytHR7W7JnxZBjnP3udsmyd+3ttHLBYmoBDYoipx7A1xg/gmwqjYCKbbprttaeYq+SqwkuctyLTsrRZvP7f4RduiFwk4PBK0DiFjWRR5QdB04t89/1O/w1cDnyilFU="
    )
    handler = WebhookHandler("8c9f8136a7b8ccd89dac2ddbd09f8597")
    body = request.get_data(as_text=True)
    json_data = json.loads(body)

    try:
        signature = request.headers["X-Line-Signature"]
        handler.handle(body, signature)
        user_id = json_data["events"][0]["source"]["userId"]
        text = json_data["events"][0]["message"]["text"]

        # 發送訊息

        # 圖庫
        if text[:3] == "img":
            api.push_message(user_id, TextSendMessage(text="圖片生成中,可能需要一點時間,請稍後..."))
            index = text.find("img")
            url_list = image.image_generator(text[index + len("img") :])
            if url_list != False:
                for i in range(4):
                    api.push_message(
                        user_id,
                        ImageSendMessage(
                            original_content_url=url_list[i],
                            preview_image_url=url_list[i],
                        ),
                    )
            else:
                api.push_message(user_id, TextSendMessage(text="圖片生成失敗,請再試一次"))
        # 油價
        elif text == "油價":
            oil.check_oil_price(user_id)
        # 天氣
        else:
            output = get_weather_info(text)
            api.push_message(user_id, TextSendMessage(text=output))
    except Exception as e:
        print(e)
    return "OK"


if __name__ == "__main__":
    app.run()
