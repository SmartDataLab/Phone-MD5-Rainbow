import pandas as pd
keyword_df = pd.read_csv("../../Msg-Post-Processing/final_filter/律政0206已标(全)_更新.csv",encoding="gbk")
#  encoding="gbk"
keyword_df

#%%
import re
filter_dict = {}
for idx in range(len(keyword_df)):
    signature = keyword_df.iloc[idx,0]
    keywords = list(keyword_df.iloc[idx,2:])
    keywords = [one for one in keywords if not pd.isna(one)]
    filter_dict[signature] = keywords
# filter_dict = {}
# sig_class_map = {}
# for idx in range(len(keyword_df)):
#     class_ = keyword_df.iloc[idx,0]
#     if pd.isna(class_):
#         continue
#     signature = keyword_df.iloc[idx,1]
#     keywords = list(keyword_df.iloc[idx,3:])
#     keywords = [one for one in keywords if not pd.isna(one)]
#     filter_dict[signature] = keywords
#     sig_class_map[signature] = class_
#%%
md5_list = []
#  single file
# with open("../../Msg-Post-Processing/data/信贷列表_左摩洋__select.csv") as f:
#     for line in f.readlines(): #[-5000:]
#         splits = line.split(",")
#         part_md5 = splits[0]
#         md5_list.append("0" * (32- len(part_md5)) + part_md5 if len(part_md5) < 32 else part_md5)

# folder
folder_path = "../../Msg-Post-Processing/data/律政0206/"


#%%
import json
# d = json.load(open("../../YQ-XY-MSG/regex_data/房车人群.json"))
d = json.load(open("../../Msg-Post-Processing/sig_database/律政.json"))
json_dict = d
#%%
sig_id_map = {key:json_dict["data"][key]["sig_id"] for key in json_dict["data"].keys()}
# %%
sig_2_id = {sig_name: detail["sig_id"] for sig_name, detail in d["data"].items()}
# %%
id_2_sig = {value:key for key,value in sig_2_id.items()}
# 74660
remove_extra_msg_sigs = """快递超市
嘀嗒出行
腾讯科技
哈啰顺风车
滴滴数科
滴滴快车
京东金融
曹操出行
滴滴出行
美团打车""".split("\n")
use_remove_extra_msg_sigs = False

if not use_remove_extra_msg_sigs:
    remove_extra_msg_sigs = []
remove_extra_msg_sig_ids = [sig_2_id[sig_name] for sig_name in remove_extra_msg_sigs]
print(list(zip(remove_extra_msg_sigs, remove_extra_msg_sig_ids)))
import os
import re
keywords = """自如网
一家和兴装饰
生活家装饰
百安居
淘赏云客
万科物业
轩尼斯门窗
万科服务家
信用家
屯粮积草网
无忧无虑家装网
不同时代
生活家家居
华耐家居
湖南合和致远
装一网
保驾护航
锡盟政务服务
尚品宅配
凤凰家博会""".split()
re_keyword = "|".join(keywords)
select_regions = set(["南京"])
select_operator = set(["移动\n"])
for file_name in os.listdir(folder_path):
    with open(folder_path + file_name, "r") as f:
        for line in f.readlines(): #[-5000:]
            splits = line.split(",")
            # if re.search(re_keyword, splits[3]):
            part_md5 = splits[0]
            content = splits[3]
            sig_id = splits[1]
            sig = id_2_sig[int(sig_id)]
            # data_df.loc[idx,"短信内容"]
            if sig not in filter_dict.keys():
                continue
            keywords = filter_dict[sig]
            re_keyword = "|".join(keywords)
            # print(keywords)
            # print(re_keyword)
            # print(content)
            # if len(keywords) != 0 and re.search(re_keyword, content)  == None:
            #     continue
                # play for shanghai bank
                ## region = splits[-1]
            # sig_id = splits[1]
            # temp_id = splits[2]
            # 最新的format处理
            region = splits[-2]
            # if int(sig_id) in remove_extra_msg_sig_ids and temp_id == "-1":
            #     continue
            operator = splits[-1]
            # print(splits)
            # if region not in select_regions:
            #     continue
            # if operator not in select_operator:
            #     continue
            md5_list.append("0" * (32- len(part_md5)) + part_md5 if len(part_md5) < 32 else part_md5)

print(len(md5_list), len(set(md5_list)))
import pickle 
# print(md5_list)
pickle.dump(set(md5_list), open("../data/md5_set.pkl","wb"))