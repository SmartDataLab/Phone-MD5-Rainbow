md5_list = []
with open("../../Msg-Post-Processing/data/贷款线索_上海_select.csv") as f:
    for line in f.readlines()[-5000:]:
        splits = line.split(",")
        part_md5 = splits[0]
        md5_list.append("0" * (32- len(part_md5)) + part_md5 if len(part_md5) < 32 else part_md5)

import pickle 
print(md5_list)
pickle.dump(set(md5_list), open("../data/md5_set.pkl","wb"))