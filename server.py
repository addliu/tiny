# -*- coding:utf-8 -*-

from wsgiref.simple_server import make_server

from hello import application

httpd = make_server('', 8080, application)
print('Serving HTTP on port 8080...')
print('Press Ctrl+C to stop server', end='\n\n')

httpd.serve_forever()
