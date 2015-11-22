from kombu import Exchange, Queue

# Broker settings.
BROKER_URL = 'amqp://iypbbgdo:80KKephngt18nEE3RW9dJOMHnpVVINLS@moose.rmq.cloudamqp.com/iypbbgdo'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('celery_app', )

# Send results back as AMQP messages
CELERY_RESULT_BACKEND = 'rpc://'

# If set to True, result messages will be persistent.
# This means the messages will not be lost after a broker restart.
CELERY_RESULT_PERSISTENT = False

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
    Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
    Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
)

# Define routes for different tasks
CELERY_ROUTES = {
    'celery_app.my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
    'celery_app.my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
    'B.add': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
}