import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

proxies = {
    'http': os.getenv('PROXY'),
    'https': os.getenv('PROXY')
}

url = 'https://www.v2ex.com/'

response = requests.get(url, proxies=proxies)

print(response.status_code)
# print(response.text)

soup = BeautifulSoup(response.text, 'html5lib')

items = []

# print(soup.find(id='TopicsHot'))
for i in soup.find_all('div', class_='cell item'):
    item = {}
    item['title'] = i.find('a', class_='topic-link').text
    item['url'] = i.find('a', class_='topic-link')['href']
    item['node'] = i.find('a', class_='node').text
    item['op'] = i.find('strong').text
    items.append(item)
    # print(item)

print(items)