with open("../data/jr_score_sort_3list_5070.txt") as f:
    lines = f.readlines()
import pickle
md5_phone_dict = pickle.load(open("../data/md5_phone_dict.pkl","rb"))
md5_set = pickle.load(open("../data/md5_set.pkl","rb"))
for line in lines:
    splits = line.strip().split(",")
    if splits[0] in md5_phone_dict.keys():
        splits = splits + [md5_phone_dict[splits[0]]]
        print(splits)
        