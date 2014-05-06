from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from resources import Root


def groupfinder(username, request):
    groups = []
    if username == 'adminuser':
        groups.append('admin')
    if username == 'manageruser':
        groups.append('manager')
    return ['g:%s' % g for g in groups]


import pymongo
from pyramid.events import NewRequest

def add_mongo_db(event):
    settings = event.request.registry.settings
    url = settings['mongodb.url']
    db_name = settings['mongodb.db_name']
    db_username = settings['mongodb.db_username']
    db_password = settings['mongodb.db_password']
    db = settings['mongodb_conn'][db_name]
    event.request.db = db


from pyramid.renderers import JSON
from bson import json_util
import json

class MongoJSONRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        request = system.get('request')
        if request is not None:
            if not hasattr(request, 'response.content_type'):
                request.response.content_type = 'application/json; charset=UTF-8'
            # set csrf token if user is logged in
            if not 'X-CSRF-Token' in request.response.headers and 'system.Authenticated' in request.effective_principals:
                request.response.headers['X-CSRF-Token'] = request.session.new_csrf_token().encode('utf-8')
        return json.dumps(value, default=json_util.default)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    my_authentication_policy = SessionAuthenticationPolicy(callback=groupfinder, debug=False)
    my_authorization_policy = ACLAuthorizationPolicy()
    
    config = Configurator(settings=settings)
    config.set_root_factory(Root)
    config.set_session_factory(my_session_factory)
    config.set_authentication_policy(my_authentication_policy)
    config.set_authorization_policy(my_authorization_policy)

    # MongoDB
    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)

    config.add_renderer('json', MongoJSONRenderer) 

    config.include('cornice')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('auth', '/auth')
    config.scan()
    return config.make_wsgi_app()
