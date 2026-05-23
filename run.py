import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request, jsonify
from backend.config.settings import config
from backend.services.search import search_service
from backend.services.speed_test import speed_tester
from backend.cache.manager import cache
from backend.utils.logger import setup_logger
import time

logger = setup_logger('api')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'frontend', 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
