import requests
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config
from utils.logger import setup_logger

logger = setup_logger('speed_test')

class SpeedTester:
    def __init__(self):
        self.timeout = config.SPEED_TEST_TIMEOUT
        self.workers = config.SPEED_TEST_WORKERS

    def test_head(self, url):
        try:
            start = time.time()
            resp = requests.head(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            elapsed = time.time() - start

            size = resp.headers.get('Content-Length', 'unknown')
            if size != 'unknown':
                size_mb = int(size) / 1024 / 1024
                size = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{int(size)/1024:.2f} KB"

            is_available = 200 <= resp.status_code < 400

            result = {
                'url': url,
                'method': 'HEAD',
                'speed': f"{elapsed:.2f}s",
                'speed_ms': int(elapsed * 1000),
                'size': size,
                'status': resp.status_code,
                'available': is_available,
                'source': urlparse(url).netloc
            }

            logger.info(f"HEAD test: {url} - {elapsed:.2f}s - {resp.status_code}")
            return result

        except requests.Timeout:
            logger.warning(f"Timeout: {url}")
            return self._error_result(url, 'timeout')
        except Exception as e:
            logger.error(f"Error: {url} - {str(e)}")
            return self._error_result(url, str(e)[:50])

    def test_range(self, url, chunk_size=1024*1024):
        try:
            start = time.time()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Range': f'bytes=0-{chunk_size-1}'
            }
            resp = requests.get(url, headers=headers, timeout=self.timeout, stream=True)

            downloaded = 0
            for chunk in resp.iter_content(chunk_size=8192):
                downloaded += len(chunk)
                if downloaded >= chunk_size:
                    break

            elapsed = time.time() - start
            speed_mbps = (downloaded / 1024 / 1024) / elapsed if elapsed > 0 else 0

            result = {
                'url': url,
                'method': 'RANGE',
                'speed': f"{speed_mbps:.2f} MB/s",
                'speed_ms': int(elapsed * 1000),
                'size': f"{downloaded/1024/1024:.2f} MB tested",
                'status': resp.status_code,
                'available': resp.status_code in [200, 206],
                'source': urlparse(url).netloc
            }

            logger.info(f"RANGE test: {url} - {speed_mbps:.2f} MB/s")
            return result

        except Exception as e:
            logger.error(f"RANGE error: {url} - {str(e)}")
            return self._error_result(url, str(e)[:50])

    def test_batch(self, urls, method='head'):
        results = []
        test_func = self.test_head if method == 'head' else self.test_range

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(test_func, url): url for url in urls}
            for future in as_completed(futures):
                results.append(future.result())

        results.sort(key=lambda x: x['speed_ms'])
        return results

    def _error_result(self, url, error):
        return {
            'url': url,
            'speed': 'error',
            'speed_ms': 999999,
            'size': 'unknown',
            'status': 0,
            'available': False,
            'source': urlparse(url).netloc,
            'error': error
        }

speed_tester = SpeedTester()
