import requests

url = 'https://gamerch.com/maimai/entry/533839'
file = 'maimai_constant.html'
headers = {
        'Accept-Language': 'ja'
        }
site_data = requests.get(url, headers=headers)
site_data.encoding = site_data.apparent_encoding
#site_data.encoding = 'utf-8'
with open(file, "wb") as f:
    f.write(site_data.content)

print("書き込み完了")
