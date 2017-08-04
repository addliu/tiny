from tiny import get, post, run_tiny


@get('/')
def index():
    return ['Indexed!'.encode('utf-8')]


@get('/hello/(?P<name>\w+)')
def personal_greeting(name=', world'):
    return ['Hello {}!'.format(name).encode('utf-8')]


run_tiny()
