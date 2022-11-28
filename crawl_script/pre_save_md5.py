md5_list = []
with open("../../Msg-Post-Processing/data/贷款线索_select.csv") as f:
    for line in f.readlines():
        splits = line.split(",")
        md5_list.append(splits[0])

import pickle 
pickle.dump(set(md5_list), open("../data/md5_set.pkl","wb"))