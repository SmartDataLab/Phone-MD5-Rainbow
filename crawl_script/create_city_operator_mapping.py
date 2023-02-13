#%%
import os
import pickle
data_dict = {}
with open("../data/city_operator_all.txt") as f:
    for line in f.readlines():
        splits = line.strip().split(",")
        data_dict[splits[0]] = splits[1:]
        # data_dict.update({key:splits[0] for key in splits[1:]})
# assign_dict = pickle.load(open("../data/assign_dict.pkl","rb"))
city = "南京"
operator ="电信"
import hashlib
from tqdm import tqdm
save_dict = {}
print()
for precode in tqdm(data_dict[city + operator]):
    for i in range(10000):
        phone_number = str(int(precode) * 10000 + i)
        hl = hashlib.md5()
        hl.update(phone_number.encode(encoding='utf-8'))
        md5 =  hl.hexdigest()
        save_dict[md5] = phone_number

import json
json.dump(save_dict,open(f"../rainbow_dict/{city}{operator}.json","w"))

