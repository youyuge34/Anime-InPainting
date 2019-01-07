import requests
import os
import traceback
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
    'Connection': 'keep-alive'
}

PROXIES = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080',
}

if __name__ == "__main__":
	url = 'http://www.getchu.com'
	r = requests.get(url,proxies = PROXIES, timeout=20, headers=HEADERS)
	# r.encoding = 'utf-8'
	print(r.text[:10])
	print(r.status_code)