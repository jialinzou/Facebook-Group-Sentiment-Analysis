from kombu import Exchange, Queue

# Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('library.data_extraction.yelp_data_extractor.yelp_extractor',
                  'library.data_extraction.facebook_data_extractor.facebook_extractor')

# Uses MongoDB as a backend
CELERY_RESULT_BACKEND = 'mongodb://localhost:27017/'

# MongoDB as a backend celery settings tensor flow
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery',
    'taskmeta_collection': 'celery_collection',
}

# If set to True, result messages will be persistent.
# This means the messages will not be lost after a broker restart.
CELERY_RESULT_PERSISTENT = True

# Accepts most of the serializers
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

# Use pickle as a serializer
CELERY_TASK_SERIALIZER = "pickle"

# The maximum number of connections that can be open in the connection pool.
BROKER_POOL_LIMIT = 0

# With the settings on, a named queue that is not already defined will get defined automatically
CELERY_CREATE_MISSING_QUEUES = False

# Set default exchange variables
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'

# Defines the queues that we can seperate tasks
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('data_extraction', Exchange('data_extraction'), routing_key='data_extraction'),
    Queue('machine_learning', Exchange('machine_learning'), routing_key='machine_learning'),
)

# Define routes for different tasks
CELERY_ROUTES = {
    'YelpExtractor.get_search_urls': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_search_info': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_business_ids': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_business_urls': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_business_info': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_business_info_urls': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.get_reviews_info': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'YelpExtractor.determine_review_pages': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
    'FacebookExtractor.get_user_posts': {'queue': 'data_extraction', 'routing_key': 'data_extraction'},
}