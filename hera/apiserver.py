from hera import api

import bottle

from bottle import request

@bottle.post('/sandbox/')
def create_sandbox():
    return get_session().create_sandbox(
        owner=request.forms['owner'],
        memory=int(request.forms['memory']),
        timeout=float(request.forms['timeout']),
        disk=int(request.forms['disk']),
    )

def get_session():
    return api.Session()

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)