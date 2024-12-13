import requests
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

api_base_url = 'https://www.v2ex.com/api/v2/'

headers = {
    'Authorization': 'Bearer ' + API_TOKEN
}

def log(func):
    def decorator(*args, **kwargs):
        response = func(*args, **kwargs)
        print(f'\033[45m[{datetime.now()}][limits: {response.headers["X-Rate-Limit-Remaining"]}][reset: {datetime.fromtimestamp(int(response.headers["X-Rate-Limit-Reset"])).strftime("%H:%M:%S")}]\033[0m', end='')
        return response.json()
    return decorator

@log
def fetch_token_status():
    url = 'https://www.v2ex.com/api/v2/token'
    response = requests.get(url=url, headers=headers)
    return response

@log
def fetch_topic(id):
    url = f'https://www.v2ex.com/api/v2/topics/{id}'
    response = requests.get(url=url, headers=headers)
    return response

@log
def fetch_reply(id):
    url = f'https://www.v2ex.com/api/v2/topics/{id}/replies'
    response = requests.get(url=url, headers=headers)
    return response

print(fetch_token_status())
print(fetch_topic(1097313))
print(fetch_reply(1097313))

