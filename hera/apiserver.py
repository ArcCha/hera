from hera import api
from hera import apimiddleware
from hera import models

import bottle
import base64

from django.core.exceptions import PermissionDenied
from bottle import request, response, default_app

default_app.push()

@bottle.post('/sandbox/')
def create_sandbox():
    return get_session().create_sandbox(
        owner=request.forms['owner'],
        memory=int(request.forms['memory']),
        timeout=float(request.forms['timeout']),
        disk=request.forms['disk'],
    )

@bottle.post('/sandbox/:id/:action')
def sandbox_action(id, action):
    return get_session().sandbox_action(
        id, action, request.forms)

@bottle.get('/template/')
def get_templates():
    owner = get_session().account
    templates = models.Template.objects.filter(owner=owner)
    return dict(status='ok', templates=[
        dict(id=template.id, name=template.name, public=template.public)
        for template in templates ])

@bottle.get('/template/:id')
def get_template(id):
    template = get_session().get_template(id, 'read')
    return dict(id=template.id, name=template.name, public=template.public, status='ok')

@bottle.post('/template/:id')
def set_template(id):
    template = get_session().get_template(id, 'write')
    new_public = request.forms.get('public', None)
    if new_public is not None:
        template.public = new_public.lower() == 'true'
    new_name = request.forms.get('name', None)
    if new_name is not None:
        template.name = new_name
    template.save()
    return {'status': 'ok'}

def get_session():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Basic '):
        response.status = 401
        response.set_header('WWW-Authenticate', 'Basic realm="use API key as password"')
        raise PermissionDenied() # TODO: do something more friendly than crashing
    user_pass = base64.b64decode(auth.split(' ')[1])
    account, _, api_key = user_pass.partition(b':')
    return api.Session(account, api_key)

app = apimiddleware.make()

if __name__ == '__main__':
    bottle.run(app=app, host='localhost', port=8080, server='waitress')
