import time
from mainPage import mainPage
from subPage import subPage
from utils.mongo_utils import mongo
from utils.redis_utils import init_redis

if __name__ == '__main__':
    db = mongo()
    r = init_redis()
    if r.get('last_id') == None:
        r.set('last_id', 0)
    while True:
        id = int(r.get('last_id')) + 1
        print(id)
        try:
            result = subPage(f'/t/{id}')
        except Exception as e:
            print(f"\033[91mERROR1\033[0m, {e}")
        if result == None:
            print(f"\033[91mERROR2\033[0m result == None {id}")
            r.sadd('none_posts', id)
            r.set('last_id', id)
            time.sleep(3)
            continue
        try:
            db.update(result)
        except Exception as e:
            print(result)
            print(f"\033[91mERROR3\033[0m, {e}")
        r.set('last_id', id)
        time.sleep(3)

