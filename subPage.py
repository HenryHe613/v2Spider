import re
import requests
from bs4 import BeautifulSoup
from utils.date_utils import parse_date

def subPage(path:str):
    def parse_subtles():
        subtles = soup.find_all('div', class_='subtle')
        for subtle in subtles:
            result['subtle'].append({
                'id': int(re.findall(r'第 (\d+) 条附言', subtle.find('span', class_='fade').text)[0]),
                'time': parse_date(subtle.find('span', class_='fade').span['title']),
                'content': subtle.find('div', class_='topic_content').text,
            })
    def parse_replies():
        replies = soup.find(id='Main').find_all('div', class_='cell')
        for reply in replies:
            if reply.get('id') == None:
                continue
            result['replies'].append({
                'id': int(reply.find('span', class_='no').text),
                'user': reply.find('strong').text,
                'time': parse_date(reply.find(class_='ago')['title']),
                'like': int(reply.find(class_='small fade').text) if reply.find(class_='small fade') != None else 0,
                'content': reply.find(class_='reply_content').text
            })
    id = re.findall(r'/t/(\d+)(?=[#\/]|$)', path)[0]
    response = requests.get(f'https://www.v2ex.com/t/{id}', allow_redirects=False)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html5lib')
    result = {
        'id': int(id),
        'user': soup.find('small', class_='gray').find('a').text,
        'title': soup.find('h1').text,
        'content': soup.find('div', class_='topic_content').text if soup.find('div', class_='topic_content') != None else None,
        'time': parse_date(soup.find('meta', attrs={'property': 'article:published_time'})['content']),
        'tag': soup.find('meta', attrs={'property': 'article:tag'})['content'],
        'section': soup.find('meta', attrs={'property': 'article:section'})['content'],
        'click': int(re.search(r'(\d+) 次点击', soup.find('small', class_='gray').text).group(1)),
        'subtle': [],
        'replies': []
    }
    parse_subtles()
    parse_replies()
    try:
        pages_url = soup.find('div', class_='ps_container').find_all('a')
        for i in range(1, len(pages_url)):
            response = requests.get(f'https://www.v2ex.com/t/{id}'+ pages_url[i]['href'])
            if response.status_code != 200:
                print("ERROR")
                continue
            soup = BeautifulSoup(response.text, 'html5lib')
            parse_replies()
    except AttributeError:
        pass
    return result

if __name__ == '__main__':
    print(subPage('/t/89'))