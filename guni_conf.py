import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
worker_class = 'gevent'
worker_connections = 2000
daemon = True
loglevel = 'info'
accesslog = 'log/gunicorn_access.log'
errorlog = 'log/gunicorn_error.log'
max_requests = 1000
graceful_timeout = 20