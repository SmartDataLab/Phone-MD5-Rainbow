#%%
import requests
resp = requests.get("https://api.xiaoxiangdaili.com/ip/get?appKey=784620260241592320&appSecret=bpga5MFD&cnt=1&wt=text")
resp
print(resp.text)
# 60.185.5.152:5021