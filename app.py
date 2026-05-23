from flask import Flask, render_template, request, jsonify
import re
import requests
from urllib.parse import urlparse, unquote, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from collections import OrderedDict

app = Flask(__name__)

def extract_filename(url):
    path = urlparse(url).path
    filename = unquote(path.split('/')[-1])
    if not filename or '.' not in filename:
        filename = 'file'
    return filename

def search_alternatives(filename, original_url):
    alternatives = [original_url]

    parsed = urlparse(original_url)
    path = parsed.path

    mirror_sites = {
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
        ]
    }

    for domain, mirrors in mirror_sites.items():
        if domain in original_url:
            for mirror in mirrors:
                if 'ghproxy' in mirror:
                    alternatives.append(mirror + original_url)
                else:
                    alternatives.append(mirror + path.lstrip('/'))

    common_mirrors = [
        'https://mirrors.tuna.tsinghua.edu.cn/',
        'https://mirrors.aliyun.com/',
        'https://mirrors.ustc.edu.cn/'
    ]

    for mirror in common_mirrors:
        if mirror not in original_url:
            test_url = mirror + filename
            alternatives.append(test_url)

    return list(dict.fromkeys(alternatives))[:15]

def test_speed(url):
    try:
        start = time.time()
        resp = requests.head(
            url,
            timeout=5,
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        elapsed = time.time() - start

        size = resp.headers.get('Content-Length', 'unknown')
        if size != 'unknown':
            size_mb = int(size) / 1024 / 1024
            size = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{int(size)/1024:.2f} KB"

        is_available = 200 <= resp.status_code < 400

        return {
            'url': url,
            'speed': f"{elapsed:.2f}s",
            'speed_ms': int(elapsed * 1000),
            'size': size,
            'status': resp.status_code,
            'available': is_available,
            'source': urlparse(url).netloc
        }
    except requests.Timeout:
        return {
            'url': url,
            'speed': 'timeout',
            'speed_ms': 999999,
            'size': 'unknown',
            'status': 0,
            'available': False,
            'source': urlparse(url).netloc,
            'error': 'timeout'
        }
    except Exception as e:
        return {
            'url': url,
            'speed': 'error',
            'speed_ms': 999998,
            'size': 'unknown',
            'status': 0,
            'available': False,
            'source': urlparse(url).netloc,
            'error': str(e)[:50]
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    url = request.json.get('url', '').strip()
    if not url:
        return jsonify({'error': '请输入下载链接'}), 400

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    filename = extract_filename(url)
    alternatives = search_alternatives(filename, url)

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(test_speed, link): link for link in alternatives}
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: x['speed_ms'])

    available_results = [r for r in results if r['available']]
    fastest = available_results[0] if available_results else None

    return jsonify({
        'filename': filename,
        'results': results,
        'fastest': fastest,
        'total': len(results),
        'available': len(available_results)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
