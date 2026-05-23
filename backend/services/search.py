from urllib.parse import urlparse, unquote
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config
from utils.logger import setup_logger

logger = setup_logger('search')

class SearchService:
    def __init__(self):
        self.max_results = config.SEARCH_MAX_RESULTS
        self.mirrors = {
            'github.com': [
                'https://ghproxy.com/',
                'https://mirror.ghproxy.com/',
                'https://gh.api.99988866.xyz/'
            ],
            'nodejs.org': [
                'https://npmmirror.com/mirrors/node/',
                'https://mirrors.tuna.tsinghua.edu.cn/nodejs-release/'
            ],
            'download.pytorch.org': [
                'https://mirrors.tuna.tsinghua.edu.cn/pytorch/whl/',
                'https://mirrors.aliyun.com/pytorch/whl/'
            ],
            'pypi.org': [
                'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/',
                'https://mirrors.aliyun.com/pypi/simple/'
            ]
        }

        self.common_mirrors = [
            'https://mirrors.tuna.tsinghua.edu.cn/',
            'https://mirrors.aliyun.com/',
            'https://mirrors.ustc.edu.cn/',
            'https://mirrors.cloud.tencent.com/'
        ]

    def extract_filename(self, url):
        path = urlparse(url).path
        filename = unquote(path.split('/')[-1])
        if not filename or '.' not in filename:
            filename = 'file'
        return filename

    def search_alternatives(self, url):
        alternatives = [url]
        parsed = urlparse(url)
        path = parsed.path
        filename = self.extract_filename(url)

        for domain, mirrors in self.mirrors.items():
            if domain in url:
                for mirror in mirrors:
                    if 'ghproxy' in mirror:
                        alternatives.append(mirror + url)
                    else:
                        alternatives.append(mirror + path.lstrip('/'))
                logger.info(f"Found {len(mirrors)} mirrors for {domain}")

        for mirror in self.common_mirrors:
            if mirror not in url:
                alternatives.append(mirror + filename)

        result = list(dict.fromkeys(alternatives))[:self.max_results]
        logger.info(f"Total alternatives: {len(result)}")
        return result

search_service = SearchService()
