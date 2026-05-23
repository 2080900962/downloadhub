import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from config.settings import config
from services.search import search_service
from services.speed_test import speed_tester
from cache.manager import cache
from utils.logger import setup_logger
import time

logger = setup_logger('api')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'frontend', 'templates')
static_dir = os.path.join(base_dir, 'frontend', 'static')

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    start_time = time.time()

    url = request.json.get('url', '').strip()
    method = request.json.get('method', 'head')

    if not url:
        return jsonify({'error': '请输入下载链接'}), 400

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    logger.info(f"Search request: {url} (method: {method})")

    cached = cache.get(url)
    if cached:
        logger.info(f"Returning cached results for {url}")
        return jsonify(cached)

    filename = search_service.extract_filename(url)
    alternatives = search_service.search_alternatives(url)

    logger.info(f"Testing {len(alternatives)} alternatives")
    results = speed_tester.test_batch(alternatives, method=method)

    available_results = [r for r in results if r['available']]
    fastest = available_results[0] if available_results else None

    response = {
        'filename': filename,
        'results': results,
        'fastest': fastest,
        'total': len(results),
        'available': len(available_results),
        'elapsed': f"{time.time() - start_time:.2f}s"
    }

    cache.set(url, response)

    logger.info(f"Search completed: {len(available_results)}/{len(results)} available in {response['elapsed']}")
    return jsonify(response)

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    cache.clear()
    return jsonify({'message': 'Cache cleared'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'cache_enabled': config.CACHE_ENABLED,
        'workers': config.SPEED_TEST_WORKERS
    })

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
