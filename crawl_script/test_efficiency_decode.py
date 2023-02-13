import json
import time
pre_t = time.time()
d = json.load(open("../rainbow_dict/南京联通.json"))
todo = list(d.keys())[:10000]
print(todo[0], d[todo[0]])
start_t = time.time()
[d[one] for one in todo]
end_t = time.time()
print(pre_t,start_t,end_t)