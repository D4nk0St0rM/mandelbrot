from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import lxml.html
import re

resp = requests.get("https://www.hbf.co.uk/directory/?filter=a&page=1")
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding)

for link in soup.find_all('a', href=True):
  
    print(link['href'])

    
    import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

for i in range(2):
    print ('i = ', i)

sys.stdout = orig_stdout
f.close()

        #don't overflow website
