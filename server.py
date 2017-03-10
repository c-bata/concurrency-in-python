import time
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


def slow_app(environ, start_response):
    time.sleep(3)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a very slow Web API']


if __name__ == '__main__':
    print("Serving on port 8000...")
    with make_server('', 8000, slow_app) as httpd:
        httpd.serve_forever()

