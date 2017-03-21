import time
from wsgiref.simple_server import make_server


def app(environ, start_response):
    time.sleep(1)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a slow web api']


if __name__ == '__main__':
    print("Serving on port 8000...")
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()

