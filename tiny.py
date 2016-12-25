# -*- coding:utf-8 -*-

"""
tiny Python 框架
参考 Daniel Lindsley 的 itty-bitty Python 框架
"""

import re

__author__ = 'addliu'
__version__ = ('0', '0', '1')
__license__ = 'MIT'

REQUEST_MAPPINGS = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'DELETE': [],
}

HTTP_MAPPINGS = {
    200: '200 OK',
    404: '404 NOT FOUND',
}


class NotFound(Exception):
    pass


class Request(object):
    def __init__(self, environ):
        self._environ = environ


def handle_request(environ, start_response):
    """The main handler. Dispatches to the user's code."""
    try:
        (re_url, url, callback), kwargs = find_matching_url(environ)
    except NotFound:
        return not_found(environ, start_response)

    request = Request(environ)
    output = callable(request, **kwargs)
    ct = 'text/html'
    status = 200

    try:
        ct = callable.content_type
    except AttributeError:
        pass

    try:
        status = callback.status
    except AttributeError:
        pass

    start_response(HTTP_MAPPINGS.get(status), [('Content-Type', ct)])
    return output


def find_matching_url(environ):
    request_method = environ.get('REQUEST_METHOD', 'GET')

    if request_method not in REQUEST_MAPPINGS:
        raise NotFound("The HTTP request method '%s' is not supported." %
                       request_method)

    path = add_slash(environ.get('PATH_INFO', ''))

    # for url_set in REQUEST_MAPPINGS[request_method].items():
    for url_set in REQUEST_MAPPINGS[request_method]:
        match = url_set[0].search(path)

        if match is not None:
            return url_set, match.groupdict()

    raise NotFound("Sorry, nothing here.")


def add_slash(url):
    if not url.endswith('/'):
        url += '/'

    return url


def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']


# Decorators

def get(url):
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)

        # Register.
        re_url = re.compile('^%s$' % add_slash(url))
        REQUEST_MAPPINGS['GET'].append((re_url, url, new))
        return new

    return wrapped


def post(url):
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)

        # Register.
        re_url = re.compile("^%s$" % add_slash(url))
        REQUEST_MAPPINGS['POST'].append((re_url, url, new))
        return new

    return wrapped


def run_tiny(host='localhost', port=8080):
    print("tiny starting up...")
    print("Use Ctrl-C to quit.", end='\n\n')

    try:
        from wsgiref.simple_server import make_server
        srv = make_server(host, port, handle_request)
        srv.serve_forever()
    except KeyboardInterrupt:
        print("Shuting down...")
        import sys
        sys.exit()


if __name__ == '__main__':
    pass
