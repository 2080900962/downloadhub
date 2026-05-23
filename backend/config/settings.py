import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True') == 'True'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))
    CACHE_DIR = os.getenv('CACHE_DIR', './data/cache')

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', './logs')

    SPEED_TEST_TIMEOUT = int(os.getenv('SPEED_TEST_TIMEOUT', 5))
    SPEED_TEST_WORKERS = int(os.getenv('SPEED_TEST_WORKERS', 10))
    SEARCH_MAX_RESULTS = int(os.getenv('SEARCH_MAX_RESULTS', 15))

    ENABLE_API_KEY = os.getenv('ENABLE_API_KEY', 'False') == 'True'
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))

config = Config()
