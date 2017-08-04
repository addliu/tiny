# -*- coding:utf-8 -*-
"""
基于Python的微型网络框架
存Python语言完成
"""
import re
__author__ = 'shanguo'
__version__ = ('0', '0', '2')


REQUEST_MAPPINGS = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'DELETE': [],
}


class NotFound(Exception):
    pass


def handle_request(environ, start_response):
    """ Application函数 """
    try:
        (re_url, url, callback), kwargs = find_matching_url(environ)
    except NotFound:
        return not_found(environ, start_response)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return callback(**kwargs)


def find_matching_url(environ):
    request_method = environ.get('REQUEST_METHOD', 'GET')

    if request_method not in REQUEST_MAPPINGS:
        raise NotFound("The HTTP request method '%s' is not supported." % request_method)

    path = add_slash(environ.get('PATH_INFO', ''))

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


# GET装饰器
def get(url):
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)

        # 设置url
        re_url = re.compile("^{}$".format(add_slash(url)))
        REQUEST_MAPPINGS['GET'].append((re_url, url, new))
        return new

    return wrapped


# POST装饰器
def post(url):
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)

        # 设置url
        re_url = re.compile("^{}$".format(add_slash(url)))
        REQUEST_MAPPINGS['POST'].append((re_url, url, new))
        return new

    return wrapped


# 简单的服务器
def run_tiny(host='localhost', port=8080):
    """
    启动tiny服务器
    接收两个可选参数
    host:  主机，默认为localhost
    port： 端口，默认为8080
    使用Python内置的WSGI实现
    """
    print("Tiny starting up ...")
    print("Use Ctrl-C to quit")
    try:
        from wsgiref.simple_server import make_server
        srv = make_server(host, port, handle_request)
        srv.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        import sys
        sys.exit()


if __name__ == '__main__':
    run_tiny()
