from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.get("https://wateroff.water.gov.tw/city/%E6%96%B0%E5%8C%97%E5%B8%82/index.html")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "/html/body/main/div/div[1]/div[2]/div[1]/select/option[10]")
    )
)
driver.find_element(
    By.XPATH, "/html/body/main/div/div[1]/div[2]/div[1]/select/option[10]"
).click()
# send_text
driver.find_element(By.CLASS_NAME, "text-input").send_keys("上田里")
# send_keys
driver.find_element(By.CLASS_NAME, "text-input").send_keys(Keys.ENTER)
