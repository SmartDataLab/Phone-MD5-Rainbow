#%%
import json
d = json.load(open("../../Msg-Post-Processing/sig_database/教育1010.json"))
json_dict = d
#%%
sig_id_map = {key:json_dict["data"][key]["sig_id"] for key in json_dict["data"].keys()}
# %%
sig_2_id = {sig_name: detail["sig_id"] for sig_name, detail in d["data"].items()}
# %%
id_2_sig = {value:key for key,value in sig_2_id.items()}
# %%
import os
folder_path = "../../Msg-Post-Processing/data/教育1115/"
files = os.listdir(folder_path)
files
#%%
import datetime 
def str_2_date(date_str):
    return  datetime.datetime(int(date_str[:4]),int(date_str[4:-2]), int(date_str[-2:])  )
one = str_2_date("20220101")
two = str_2_date("20220102")

one < two < str_2_date("20220103")
def filter_date_range(files, start_date_str, end_date_str):
    start_date = str_2_date(start_date_str)
    end_date = str_2_date(end_date_str)
    return [file  for file in files if start_date <= str_2_date(file.split(".")[1]) <= end_date]
#%%
one_week_files = filter_date_range(files, "20221013","20221020")
half_month_files = filter_date_range(files, "20221005","20221020")
one_month_files = filter_date_range(files, "20220920","20221020")
two_month_files = filter_date_range(files, "20220820","20221020")
#%%
import pickle
md5_phone_dict = pickle.load(open("../data/md5_phone_dict.pkl","rb"))
# %%
select_province = set(["北京", "成都", "广州"]+[ "沈阳" , "大连"] + ["广州"] + ["北京", "天津","太原"] + ["济宁","济南","青岛", "合肥", "苏州","杭州","福州","无锡"] + ["武汉","长沙","郑州"] +["西安"] +["成都","重庆","贵阳","昆明","南充"])
keywords = [ "按摩","推拿" ] + "艾草OR肩颈OR膏药OR按摩椅OR筋膜枪OR舒筋OR活血OR保健OR护颈OR足浴OR精油OR经络OR疏通".split("OR") + "骨科OR骨OR创伤OR外科OR康复OR中医OR保健OR挂号".split("OR")
re_keyword = "|".join(keywords)
from collections import Counter
from tqdm import tqdm
import re
cnt_all = Counter()
md5_list = [ ]
select_all =[]
cnt_province = Counter()
for file in tqdm(one_month_files):
    with open(folder_path + file) as f:
        select_list = []
        for one in f.readlines():
            splits = one.split(",")
            # if re.search(re_keyword, splits[3]):
            # some md5 dict may not prepare well
            if splits[0] in md5_phone_dict.keys():
                cnt_province[splits[-3]] += 1
                name = id_2_sig[int(splits[1])]
                if splits[2] == "-1":
                    regex = splits[3]
                else:
                    regex = json_dict["data"][name]["template"][int(splits[2])-1]["regex"]
                # if  splits[-3] in select_province:
                select_list.append(",".join([md5_phone_dict[splits[0]]] + splits[1:-1] + [regex+"\n"]))
                md5_list.append(splits[0])
        cnt = Counter(select_list)
        select_all += select_list
    cnt_all.update(cnt)
#%%
with open("../data/核桃_2w5.csv","w") as f:
    f.writelines(select_all)
 
# %%
