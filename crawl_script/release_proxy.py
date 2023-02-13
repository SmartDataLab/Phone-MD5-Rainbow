
import requests
proxy_ip = "211.93.121.182:5021"
post_url = f"https://api.xiaoxiangdaili.com/ip/release?appKey=784620260241592320&appSecret=bpga5MFD&proxy={proxy_ip}"
resp = requests.post(post_url)
resp
# notices to 
# ban ip_list
# 223.242.223.251:5021
# 211.93.123.62:5021
# 61.191.85.52:5021
# 49.84.170.170:5021
# 211.93.121.182:5021
# 49.67.42.180:5021
print(resp.text)