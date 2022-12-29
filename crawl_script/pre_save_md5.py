md5_list = []
#  single file
# with open("../../Msg-Post-Processing/data/信贷列表_左摩洋__select.csv") as f:
#     for line in f.readlines(): #[-5000:]
#         splits = line.split(",")
#         part_md5 = splits[0]
#         md5_list.append("0" * (32- len(part_md5)) + part_md5 if len(part_md5) < 32 else part_md5)

# folder
folder_path = "../../Msg-Post-Processing/data/房车公积金1221/"



import json
d = json.load(open("../../YQ-XY-MSG/regex_data/房车人群.json"))
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
remove_extra_msg_sig_ids = [sig_2_id[sig_name] for sig_name in remove_extra_msg_sigs]
print(list(zip(remove_extra_msg_sigs, remove_extra_msg_sig_ids)))
import os
select_regions = set(["上海","南京"])
for file_name in os.listdir(folder_path):
    with open(folder_path + file_name, "r") as f:
        for line in f.readlines(): #[-5000:]
            splits = line.split(",")
            part_md5 = splits[0]
            sig_id = splits[1]
            temp_id = splits[2]
            # 最新的format处理
            region = splits[-2]
            if int(sig_id) in remove_extra_msg_sig_ids and temp_id == "-1":
                continue
            if region not in select_regions:
                continue
            md5_list.append("0" * (32- len(part_md5)) + part_md5 if len(part_md5) < 32 else part_md5)

print(len(md5_list), len(set(md5_list)))
import pickle 
# print(md5_list)
pickle.dump(set(md5_list), open("../data/md5_set.pkl","wb"))