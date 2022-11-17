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
import time
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4324.104 Safari/537.36')
chromeOptions.add_argument('--start-maximized')
chromeOptions.add_argument('window-size=1400,900')
driver = webdriver.Chrome(service=service, options=chromeOptions)
# %%
driver.get("https://tool.ytxsvr.com/md5")
# %%

def get_one_phone_number(md5):
    input_el = driver.find_element_by_class_name("el-input__inner")
    input_el.clear()
    input_el.send_keys(md5)
    decrypt_btn = driver.find_elements_by_class_name("el-button--default")[1]
    # decrypt_btn = driver.find_elements_by_class_name("el-button--default")[0]
    # time.sleep(0.1)
    decrypt_btn.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "el-alert__title")))
    # time.sleep(0.1)
    result_el = driver.find_elements_by_class_name("el-alert__title")[0]
    return result_el.text
get_one_phone_number("e693a91a798cf0235c3d61751e650c3b")
#%%
get_one_phone_number("7f7c0bf3b7c33e80e660a9e92a79ec70")
#%%
driver.get_screenshot_as_file("../save.png")
# %%

import os
# with open("../data/ETC_sms02_8_sms01_7.ETC.filter") as file:
#     lines = file.readlines()
# %%

# lines[0]
# %%
file_folder = "../../Msg-Post-Processing/data/教育1115/"
md5_set = set()
for file in os.listdir(file_folder):
    with open(file_folder + file) as file:
        lines = file.readlines()
    md5_set = md5_set.union(set([line.split(",")[0] for line in lines]))
len(md5_set)
#%%
with open("/Users/su/Downloads/会计人群包_最近60天.txt") as file:
    md5_set = [one.replace("\n", "") for one in file.readlines()]
with open("/Users/su/Downloads/会计人群包_最近15天.txt") as file:
    md5_set_last = [one.replace("\n", "") for one in file.readlines()]
md5_set = list(set(md5_set) - set(md5_set_last))
#%%
with open("../data/zhuangxiu_city_select.filter") as file:
    md5_set = [one.split(",")[0] for one in file.readlines()]
#%%
md5_set
# %%

md5_phone_dict = {}
import  pickle
# md5_phone_dict = pickle.load(open("../data/zhuangxiu.pkl","rb"))
#%%
from tqdm import tqdm
for md5 in tqdm(md5_set):
    if md5 in md5_phone_dict.keys():
        continue
    result = get_one_phone_number(md5)
    if result == '请输入有效的md5值!':
        print("错误", result)
    
    md5_phone_dict[md5] = result
#%%
import pickle
pickle.dump(md5_phone_dict, open("../data/md5_phone_dict.pkl","wb"))
pickle.dump(md5_set, open("../data/md5_set.pkl","wb"))
#%%

write_file = open("../data/会计人群包_最近60天_phone_number.csv","w")
for file in os.listdir(file_folder):
    with open(file_folder + file) as file:
        lines = file.readlines()
    for line in lines:
        new_line = md5_phone_dict[line.split(',')[0]] + "," + ",".join(line.split(',')[1:]) 
        # new_line = md5_phone_dict[line.split(',')[0]] + "\n" + ",".join(line.split(',')[1:]) 
        write_file.write(new_line)
    # md5_set = md5_set.union(set([line.split(",")[0] for line in lines]))
#%%

with open("../data/zhuangxiu_all.filter") as f:
    lines = f.readlines()
# %%
new_lines = []
for line in lines:
    new_line = md5_phone_dict[line.split(',')[0]] + "," + ",".join(line.split(',')[1:]) 
    new_lines.append(new_line)
#%%
with open("../data/zhuangxiu_all.csv","w") as f:
    f.writelines(new_lines)
# %%
with open("../data/会计人群包_最近60天_phone_number.csv","w") as f:
    f.writelines([one + "\n" for one in md5_phone_dict.values()])
# %%

with open("../data/ETC.csv","w") as f:
    f.writelines(new_lines)
# %%
# change into multi processing
# https://blog.csdn.net/zwq912318834/article/details/78962648