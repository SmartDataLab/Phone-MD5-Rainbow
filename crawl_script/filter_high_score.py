import pandas as pd
file_path = "../data/jr_score_sort_3list.csv"
with open(file_path) as f:
    lines = f.readlines()
md5_set =[]
for line in lines:
    splits = line.split(",")
    if int(splits[1]) > 80:
        md5_set.append(splits[0])
print(len(md5_set),len(set(md5_set)))

import pickle 
pickle.dump(set(md5_set), open("../data/md5_set.pkl","wb"))
        