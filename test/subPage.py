import requests
from dotenv import load_dotenv
import os
import re
from bs4 import BeautifulSoup

load_dotenv()

proxies = {
    'http': os.getenv('PROXY'),
    'https': os.getenv('PROXY')
}

def subPage(path:str, subPageNext:bool=False):
    url = 'https://www.v2ex.com' + path
    response = requests.get(url, proxies=proxies)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html5lib')
    result = {
        'content': soup.find(class_='markdown_body').text,
        'time': soup.find(class_='gray').find('span')['title'],
        'replies': []
    }
    replies = soup.find(id='Main').find_all('div', class_='cell')
    for reply in replies:
        if reply.get('id') == None:
            continue
        result['replies'].append({
            'user': reply.find('strong').text,
            'date': reply.find(class_='ago')['title'],
            'like': int(reply.find(class_='small fade').text) if reply.find(class_='small fade') != None else 0,
            'id': reply.find('span', class_='no').text,
            'content': reply.find(class_='reply_content').text
        })
    if not subPageNext:
        reply_counts = re.findall(r'#reply(\d+)$', path)[0]
        page_id = re.findall(r'/t/(\d+)#reply\d+', path)[0]
        print(page_id)
        for i in range(2, (int(reply_counts)-1)//100+2):
            result['replies'].extend(subPage(f'/t/{page_id}?p={i}', True)['replies'])
    print(result)
    return result

if __name__ == '__main__':
    subPage('/t/1094129#reply109')