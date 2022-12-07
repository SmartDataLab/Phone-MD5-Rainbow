# 直接创建字典是可以的
data_dict = {}
with open("../data/city_operator_all.txt") as f:
    for line in f.readlines():
        splits = line.strip().split(",")
        data_dict.update({key:splits[0] for key in splits[1:]})
len(data_dict)


import pickle 
pickle.dump(data_dict,open("../data/assign_dict.pkl","wb"))