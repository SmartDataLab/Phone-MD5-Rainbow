
#%%
# import configure
import multiprocessing
import time
import pickle
WORKER_NUM = 10

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
service = Service(executable_path=ChromeDriverManager().install())
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4324.104 Safari/537.36')
chromeOptions.add_argument('--start-maximized')
chromeOptions.add_argument('window-size=1400,900')
drivers = [webdriver.Chrome(service=service, options=chromeOptions) for _ in range(WORKER_NUM)]
[driver.get("https://tool.ytxsvr.com/md5") for driver in drivers]
#%%
import pickle
md5_set = pickle.load(open("../data/md5_set.pkl","rb"))
md5_phone_dict = pickle.load(open("../data/md5_phone_dict.pkl","rb"))

# %%

def get_one_phone_number(md5, driver):
    input_el = driver.find_element_by_class_name("el-input__inner")
    input_el.clear()
    input_el.send_keys(md5)
    decrypt_btn = driver.find_elements_by_class_name("el-button--default")[1]
    decrypt_btn.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "el-alert__title")))
    result_el = driver.find_elements_by_class_name("el-alert__title")[0]
    return result_el.text


#%%
# 由mark标记是哪个进程执行的动作
def getPhoneNumberFunc(queue, lock, mark, res_queue):
    count = 0 
    while not queue.empty():
        # def get(self, block=True, timeout=None):
        md5 = queue.get()
        # 加锁，是为了防止散乱的打印。 保护一些临界状态
        # 多个进程运行的状态下，如果同一时刻都调用到print，那么显示的打印结果将会混乱
        # print(f"keyWord = {keyWord}, markProcess = {mark}")
        # if md5 in md5_phone_dict.keys():
        #     continue
        result = get_one_phone_number(md5, drivers[mark]) 
        
        lock.acquire()
        print(count ,result)
        if result == '请输入有效的md5值!':
            print("错误", result)
        lock.release()
        count += 1
        res_queue.put((md5, result))

from tqdm import tqdm
# if __name__ == '__main__':
lock = multiprocessing.Lock()       # 进程锁
queue = multiprocessing.Queue(600000)  # 队列，用于存放所有的初始关键字
res_queue = multiprocessing.Queue(600000)  # 队列，用于存放所有的初始关键字
# queue.
for md5 in md5_set:
    if md5 not in md5_phone_dict.keys():
    # print(f"keyWord = {keyWord}")
    # 如果queue定的太小，剩下的放不进去，程序就会block住，等待队列有空余空间
    # def put(self, obj, block=True, timeout=None):
    # print(md5)
        queue.put(md5)
print(f"queueBefore = {queue}")
getKeyProcessLst = []
queue_list = [ ]
# 生成两个进程，并启动
for i in range(WORKER_NUM):
    # 携带的args 必须是python原有的数据类型，不能是自定义的。否则会出现下面的error（见后面）
    process = multiprocessing.Process(target = getPhoneNumberFunc, args = (queue, lock, i, res_queue))
    process.start()
    getKeyProcessLst.append(process)
write_f = open("../data/write_tmp.txt","w") 
# 关不上进程
for th_item in getKeyProcessLst:
    while th_item.is_alive():
        while False == res_queue.empty():
            one = res_queue.get()
            write_f.write(one[0] + " " + one[1] + "\n")
            queue_list.append(one)
# 守护线程
# join 等待线程终止，如果不使用join方法对每个线程做等待终止，那么线程在运行过程中，可能会去执行最后的打印
# 如果没有join，父进程就不会阻塞，启动子进程之后，父进程就直接执行最后的打印了
for p in getKeyProcessLst:
    p.join()

print(f"queueAfter = {queue}")
queue.close()
print(f"all queue used.")

# %%
# queue_list = [ res_queue.get() for _ in range(res_queue.qsize())]
# %%
queue_list
# %%
for md5, phone in queue_list:
    md5_phone_dict[md5] = phone
# %%
len(md5_phone_dict)
# %%
len(md5_set)
# %%

pickle.dump(md5_phone_dict, open("../data/md5_phone_dict.pkl","wb"))
# %%
import pickle
md5_set = pickle.load(open("../data/md5_set.pkl","rb"))
md5_phone_dict = pickle.load(open("../data/md5_phone_dict.pkl","rb"))
#%%

read_f = open("../data/write_tmp.txt","r")
lines = read_f.readlines()
# %%
new_dict = {line.strip().split()[0]:line.strip().split()[1] for line in lines}
new_dict
# %%
md5_phone_dict.update(new_dict)
# %%
pickle.dump(md5_phone_dict, open("../data/md5_phone_dict.pkl","wb"))
# %%
