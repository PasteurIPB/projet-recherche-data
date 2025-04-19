python
import os

# Configuration de la base de données
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Configuration du cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': os.environ.get('REDIS_HOST'),
    'CACHE_REDIS_PORT': os.environ.get('REDIS_PORT'),
}

# Configuration des langues
BABEL_DEFAULT_LOCALE = 'fr'
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'fr': {'flag': 'fr', 'name': 'French'},
}