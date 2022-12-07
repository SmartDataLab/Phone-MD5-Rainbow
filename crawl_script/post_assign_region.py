#
# with open("../data/南京号段.txt") as f:
#     lines = [line.strip().replace("南京", "") for line in f.readlines()]
# region_codes = set(lines)
import pickle
with open("../data/write_tmp.txt") as f:
    lines = f.readlines()
    md5_phone_dict = {line.split()[0]:line.split()[1].strip() for line in lines}
# print(region_codes)
# select_dict = {}
# for md5, phone_num in md5_phone_dict.items():
#     if phone_num[3:7] in region_codes:
#         select_dict[md5] = phone_num
# len(select_dict)
import pickle 
assign_dict = pickle.load(open("../data/assign_dict.pkl","rb"))
file_path = "../data/jr_score_sort_3list.csv"
with open(file_path) as f:
    new_lines = f.readlines()
output_lines = []
for line in new_lines:
    splits = line.split(",")
    # if splits[0] in select_dict.keys():
    if int(splits[1]) < 80:
        continue
    
    try:
        phone_num = md5_phone_dict[splits[0]]
        assign_region = assign_dict[phone_num[:7]]
        new_line = [phone_num , assign_region] + splits[1:]
        output_lines.append(",".join(new_line))
    except Exception as e:
        print(line)

with open("../data/80_all.csv","w") as f:
    f.writelines(set(output_lines))