import os

with open("../data/小学教育签名.sig") as f:
    sigs = f.readlines()

sigs = set([line.strip() for line in sigs])



import json
d  =  json.load(open('../../Msg-Post-Processing/sig_database/小学教育.json'))
json_dict = d 
sig_id_map = {key:json_dict["data"][key]["sig_id"] for key in json_dict["data"].keys()}
sig_2_id = {sig_name: detail["sig_id"] for sig_name, detail in d["data"].items()}
id_2_sig = {value:key for key,value in sig_2_id.items()}

sigs_id = set([str(sig_2_id[sig]) for sig in sigs])

md5_list = []
with open("../../Msg-Post-Processing/data/小学教育_all.csv") as f:
    for line in f.readlines():
        splits = line.split(",")
        if splits[1] in sigs_id:
            md5_list.append(splits[0])

import pickle 
pickle.dump(set(md5_list), open("../data/md5_set.pkl","wb"))