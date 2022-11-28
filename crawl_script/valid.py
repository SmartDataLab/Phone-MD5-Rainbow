import os
folder = "../../Msg-Post-Processing/data/贷款线索1126/"
files = os.listdir(folder)
files
from collections import Counter
all_cnt = Counter()
from tqdm import tqdm
for file_ in tqdm(files):
    with open(folder + file_) as f:
        # if len len(line.split(",")[0]
        # cnt = Counter([len(line.split(",")[0]) for line in f.readlines()])
        for line in f.readlines():
            if len(line.split(",")[0]) < 32:
                print(line)
        exit()
        all_cnt.update(cnt)
        print(cnt.most_common())
print(all_cnt.most_common())