import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
from datetime import datetime as dt
import pytz

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("headless")
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("window-size=1920,1080")


URL = 'https://markets.ft.com/data/search?assetClass=Fund'
DATE_TODAY = dt.now(tz=pytz.timezone("Asia/Manila")).date()
DIRECTORY = f"ISINs_{DATE_TODAY}"

class DataModel:
    def __init__(self, symbol, xid):
        self.symbol = symbol
        self.xid = xid
    def result(self):
        return self.__dict__

def search_securities(ISIN):
    browser = webdriver.Chrome(r"/chromedriver_linux64/chromedriver", chrome_options=chrome_options)
    browser.get(URL)
    # browser.maximize_window()
    elem = browser.find_element(By.NAME, 'query')  # Find the search box
    elem.send_keys(f"{ISIN}", Keys.ENTER)
    elems = browser.find_elements(By.XPATH, "//*[contains(@data-oda, 'tearsheet')]")
    print("length: ", len(elems))
    if (len(elems) != 1) & (len(elems) > 0):
        print(f"too many search result: {ISIN}")
        elems = [elems[0]]
    if len(elems) == 0:
        print("no results found")
        return 
    for elem in elems:
        elem.click()
        sleep(1)
        element = browser.find_element(By.XPATH, "//section[contains(@data-mod-config, 'xid')]")
        xid = json.loads(element.get_attribute("data-mod-config")).get("xid")
        symbol = json.loads(element.get_attribute("data-mod-config")).get("symbol")
        data = DataModel(symbol, xid).result()
        browser.close()
        return data    


def main():
    # print(DATE_TODAY)
    if not os.path.isdir(DIRECTORY):
        os.mkdir(DIRECTORY)
    
    isins = pd.read_csv("reference_files/ISINs (2).csv")
    isins = isins["ISIN"].values
    xid_list = []
    no_result = []
    count = 0
    for isin in isins:
        data = search_securities(isin)
        if data:
            xid_list.append(data)
        count+=1
        print(count)
        print(data)
    xid_list = pd.DataFrame(data=xid_list)
    print(f"{DIRECTORY}/xid_list.csv")
    xid_list.to_csv(f"{DIRECTORY}/xid_list.csv", index=False)
    # print(no_result)

main()