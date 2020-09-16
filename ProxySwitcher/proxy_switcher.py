import requests

proxies = {
 'http': 'http://10.10.10.10:8000',
 'https': 'http://10.10.10.10:8000'
}

r = requests.get('http://toscrape.com', proxies=proxies)
