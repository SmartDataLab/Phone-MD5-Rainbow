#%%
import pickle
continue_use = False
if continue_use:
    md5_phone_dict = pickle.load(open("../data/md5_phone_dict.pkl","rb"))
else:
    md5_phone_dict = {}

md5_phone_dict = {key:value for key,value in md5_phone_dict.items() if len(value) == 11}
#%%
print(len(md5_phone_dict))
#%%
standard_len = 32 + 1 + 11 + 1
read_file_path = "../data/write_tmp.txt"
with open(read_file_path) as f:
    md5_phone_dict.update({line[:32]:line[-12:-1] for line in f.readlines() if len(line) == standard_len})
print(len(md5_phone_dict))
pickle.dump(md5_phone_dict,open("../data/md5_phone_dict.pkl","wb"))