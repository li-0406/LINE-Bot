import threading
import warnings
import subprocess
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from flask import Flask, request
from linebot.models import TextSendMessage, ImageSendMessage
from linebot import LineBotApi, WebhookHandler, LineBotSdkDeprecatedIn30


def image_generator(text):
    # 不希望在使用到一半時直接看到瀏覽器的畫面
    options = Options()
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    api = LineBotApi(
        "lzAAH48tUDN4ovgVj/O3HAJHwUuBCLjhLc14vuxs7dx7lHytHR7W7JnxZBjnP3udsmyd+3ttHLBYmoBDYoipx7A1xg/gmwqjYCKbbprttaeYq+SqwkuctyLTsrRZvP7f4RduiFwk4PBK0DiFjWRR5QdB04t89/1O/w1cDnyilFU="
    )

    try:
        driver = webdriver.Chrome()
        driver.get("https://www.bing.com/images/create?FORM=GENILP")

        # 此處參考 https://heykush.hashnode.dev/add-cookies-in-selenium
        with open("./cookie.json", "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                if "sameSite" in cookie:
                    cookie["sameSite"] = "Strict"
                driver.add_cookie(cookie)
        time.sleep(3)
        # 重新刷新以讀取cookie資訊
        driver.refresh()

        # 尋找搜尋輸入欄並輸入搜尋訊息
        driver.find_element(By.ID, "sb_form_q").send_keys(text)
        driver.find_element(By.ID, "create_btn_c").click()

        locate_pos = (By.XPATH, "/html/body/div[3]/div/div[5]/div[1]/div[2]/div/div")

        # 等待生成圖片...
        WebDriverWait(driver, 200).until(EC.presence_of_element_located(locate_pos))

        # 定位每張照片的位置
        pic_url_list = []
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'ul[data-row="0"] li[data-idx="1"] div div a div img')
            )
        )

        # 取得每張圖片的連結
        pic_1 = driver.find_element(
            By.CSS_SELECTOR, 'ul[data-row="0"] li[data-idx="1"] div div a div img'
        ).get_attribute("src")
        pic_url_list.append(pic_1 + ".jpg")

        pic_2 = driver.find_element(
            By.CSS_SELECTOR, 'ul[data-row="0"] li[data-idx="2"] div div a div img'
        ).get_attribute("src")
        pic_url_list.append(pic_2 + ".jpg")

        pic_3 = driver.find_element(
            By.CSS_SELECTOR, 'ul[data-row="1"] li[data-idx="3"] div div a div img'
        ).get_attribute("src")
        pic_url_list.append(pic_3 + ".jpg")

        pic_4 = driver.find_element(
            By.CSS_SELECTOR, 'ul[data-row="1"] li[data-idx="4"] div div a div img'
        ).get_attribute("src")
        pic_url_list.append(pic_4 + ".jpg")

        print(pic_url_list)

        return pic_url_list

    except Exception as e:
        print(e)
        return False


# image_generator("台北101")
