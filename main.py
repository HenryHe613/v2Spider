import time
from mainPage import mainPage
from subPage import subPage
from utils.log_utils import LOG
from utils.mongo_utils import mongo
from utils.redis_utils import init_redis

if __name__ == '__main__':
    db = mongo()
    logger = LOG('main', LOG.DEBUG).logger
    r = init_redis()
    if r.get('last_id') == None:
        r.set('last_id', 0)
    while True:
        id = int(r.get('last_id')) + 1
        logger.info(f"{id}")
        try:
            result = subPage(f'/t/{id}')
        except Exception as e:
            logger.error(f"1 {e}")
        if result == None:
            logger.error(f"result == None {id}")
            r.sadd('none_posts', id)
            r.set('last_id', id)
            time.sleep(3)
            continue
        try:
            db.update(result)
        except Exception as e:
            logger.info(result)
            logger.error(f"3 {e}")
        r.set('last_id', id)
        time.sleep(3)

