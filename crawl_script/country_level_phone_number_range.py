#%%
import requests
from scrapy import Selector
#%%
# page_range = range(8)
# name_list = []
# url_list = [] 
# for page_num in page_range:
#     resp = requests.get(f"https://www.chahaoba.cn/city/%E9%8D%97%E6%A4%BE%E5%90%AB%E7%94%AF?page={page_num}")
#     sel = Selector(text = resp.content)
#     name_list += sel.css("div.item-list ol li div span a::text").getall() 
#     url_list += sel.css("div.item-list ol li div span a::attr(href)").getall() 

# len(url_list)

# specific_base  =  "https://www.chahaoba.cn/city"


# resp = requests.get(specific_base + url_list[0])
# sel = Selector(text = resp.content)

#%%
city_operator_names  = [] 
city_operator_urls  =  [] 
operator_page_range = range(6)
for operator_page_num in operator_page_range:
    operator_url = f"https://www.chahaoba.cn/city-operator-list?page={operator_page_num}"
    resp = requests.get(operator_url)
    sel = Selector(text = resp.content)
    city_operator_names  += sel.css("div.view-grouping-content div.field-content a::text").getall()
    city_operator_urls  += sel.css("div.view-grouping-content div.field-content a::attr(href)").getall()

# %%
# 有点慢
# 
import multiprocessing
import time
import pickle
from tqdm import tqdm
from collections import defaultdict
WORKER_NUM = 10
lock = multiprocessing.Lock()       # 进程锁
queue = multiprocessing.Queue(600000)  # 队列，用于存放所有的初始关键字
res_queue = multiprocessing.Queue(600000) 

data_dict = defaultdict(list)
url_base = "https://www.chahaoba.cn"
def get_one_city_operator_phone_number(city_operator_url):
    resp = requests.get(url_base + city_operator_url)
    sel = Selector(text = resp.content)
    city_top3_names  = sel.css("div.view-grouping-content div.field-content a::text").getall()
    city_top3_urls  = sel.css("div.view-grouping-content div.field-content a::attr(href)").getall()
    tmp_list = []
    for city_top3_url in city_top3_urls:
        resp = requests.get(url_base + city_top3_url)
        sel = Selector(text = resp.content)
        phone_top7s = sel.css("div.view-content tbody tr td.views-field.views-field-title a::text").getall()
        tmp_list += phone_top7s
    return tmp_list
    
for city_operator_name, city_operator_url in tqdm(zip(city_operator_names, city_operator_urls)):
    queue.put((city_operator_name,city_operator_url))
    # data_dict[city_operator_name] = get_one_city_operator_phone_number(city_operator_url)
print(f"queueBefore = {queue}")
getKeyProcessLst = []
queue_list = [ ]

def getPhoneNumberFunc(queue, lock, mark, res_queue):
    count = 0 
    while not queue.empty():
        # def get(self, block=True, timeout=None):
        city_operator_name, city_operator_url = queue.get()
        # 加锁，是为了防止散乱的打印。 保护一些临界状态
        # 多个进程运行的状态下，如果同一时刻都调用到print，那么显示的打印结果将会混乱
        # print(f"keyWord = {keyWord}, markProcess = {mark}")
        # if md5 in md5_phone_dict.keys():
        #     continue
        result = get_one_city_operator_phone_number(city_operator_url)
        # result = get_one_phone_number(md5) 
        lock.acquire()
        print(count)
        lock.release()
        count += 1
        res_queue.put((city_operator_name, result))


for i in range(WORKER_NUM):
    # 携带的args 必须是python原有的数据类型，不能是自定义的。否则会出现下面的error（见后面）
    process = multiprocessing.Process(target = getPhoneNumberFunc, args = (queue, lock, i, res_queue))
    process.start()
    getKeyProcessLst.append(process)
write_f = open("../data/city_operator_all.txt","w") 
# 关不上进程
for th_item in getKeyProcessLst:
    while th_item.is_alive():
        while False == res_queue.empty():
            (city_operator_name,phone_top7s) = res_queue.get()
            write_f.write(city_operator_name + "," + ",".join(phone_top7s) + "\n")
            # queue_list.append(one)
# 守护线程
# join 等待线程终止，如果不使用join方法对每个线程做等待终止，那么线程在运行过程中，可能会去执行最后的打印
# 如果没有join，父进程就不会阻塞，启动子进程之后，父进程就直接执行最后的打印了
for p in getKeyProcessLst:
    p.join()