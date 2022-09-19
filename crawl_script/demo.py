#%%
import requests
url = "https://tool.ytxsvr.com:18201/1?rid=901c48aa-36e0-460b-b1d4-32b844fcbd27"
data = {"uid":"9dbbe80b-c098-4b88-a520-b276ff60a325","password":"8a99b9f39c0af51cd1043fa650363348","timestamp":"20220919102529","type":2,"content":"e693a91a798cf0235c3d61751e650c3b","requestId":"ee821176-aaf1-41dd-81f5-fc0d9081bf8e"}
resp = requests.post(url, data=data)
resp.content
# %%
# password
# requestid
# timestamp
# inpage.js
# 需要反混淆了，目前搜了几个关键词，感觉不对，再搜几个
# 暂时看不出来
#%%
from selenium import webdriver


driver = webdriver.Firefox()
driver.get(url)
# %%
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
service = Service(executable_path=ChromeDriverManager().install())
# service = Service(
#     executable_path="/home/su/.wdm/drivers/chromedriver/linux64/105.0.5195.52/chromedriver"
# )
# service = Service(executable_path=ChromeDriverManager())
#%%
driver = webdriver.Chrome(service=service)
# %%
