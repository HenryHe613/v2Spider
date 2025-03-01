import requests
from bs4 import BeautifulSoup
from utils.date_utils import parse_date

def mainPage(url:str='https://www.v2ex.com/?tab=all'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    topics = {
        'hot': [],
        'latest': [],
    }
    for i in soup.find_all('div', class_='cell item'):
        topics['latest'].append({
            'title': i.find('a', class_='topic-link').text,
            'url': i.find('a', class_='topic-link')['href'],
            'node': i.find('a', class_='node').text,
            'op': i.find('strong').text,
            'time': parse_date(i.find('span', class_='topic_info').find('span')['title']),
        })
    for i in soup.find('div', id='TopicsHot').find_all('table'):
        topics['hot'].append({
            'title': i.find('span', class_='item_hot_topic_title').find('a').text,
            'url': i.find('span', class_='item_hot_topic_title').find('a')['href']
        })
    return topics

if __name__ == '__main__':
    print(mainPage())
