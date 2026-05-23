import json
import os
import hashlib
import time
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config
from utils.logger import setup_logger

logger = setup_logger('cache')

class Cache:
    def __init__(self):
        self.enabled = config.CACHE_ENABLED
        self.ttl = config.CACHE_TTL
        self.cache_dir = config.CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_key(self, url):
        return hashlib.md5(url.encode()).hexdigest()

    def _get_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, url):
        if not self.enabled:
            return None

        key = self._get_key(url)
        path = self._get_path(key)

        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if time.time() - data['timestamp'] > self.ttl:
                os.remove(path)
                logger.info(f"Cache expired: {url}")
                return None

            logger.info(f"Cache hit: {url}")
            return data['results']
        except:
            return None

    def set(self, url, results):
        if not self.enabled:
            return

        key = self._get_key(url)
        path = self._get_path(key)

        data = {
            'url': url,
            'timestamp': time.time(),
            'results': results
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Cache saved: {url}")

    def clear(self):
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))
        logger.info("Cache cleared")

cache = Cache()
