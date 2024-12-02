import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

proxies = {
    'http': os.getenv('PROXY'),
    'https': os.getenv('PROXY')
}

url = 'https://www.v2ex.com/t/1094129#reply60'

response = requests.get(url, proxies=proxies)

print(response.status_code)
# print(response.text)

soup = BeautifulSoup(response.text, 'html5lib')

items = []

print(soup.find(class_='markdown_body').text) # main content

print(soup.find(class_='gray').find('span')['title']) # time

print(len(soup.find_all('tbody')))

replies = []

for i in soup.find_all('tbody'):
    reply = {}
    reply['user'] = i.find('strong').text
    reply['date'] = i.find(class_='ago')['title']
    reply['like'] = int(i.find(class_='small fade').text) if i.find(class_='small fade') != None else 0
    reply['id'] = i.find('span', class_='no').text
    reply['content'] = i.find(class_='reply_content').text
    replies.append(reply)

print(replies)