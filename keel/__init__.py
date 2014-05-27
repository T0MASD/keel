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

    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    conn = MongoDB(db_uri)
    settings['mongodb_conn'] = conn
    
    db_name = settings['mongodb.db_name']
    db_username = settings['mongodb.db_username']
    db_password = settings['mongodb.db_password']
    db = settings['mongodb_conn'][db_name]
    event.request.db = db


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': request.environ['HTTP_ORIGIN'] if 'HTTP_ORIGIN' in request.environ else "*",
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS,PATCH',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        'Access-Control-Expose-Headers': 'X-Toaster-Notification, X-CSRF-Token',
        })
    event.request.add_response_callback(cors_headers)


def add_csrf_token_header(event):
    def csrf_token_header(request, response):
        if not 'X-CSRF-Token' in response.headers and 'system.Authenticated' in request.effective_principals:
            response.headers.update({
                'X-CSRF-Token':request.session.new_csrf_token().encode('utf-8')
                })
    event.request.add_response_callback(csrf_token_header)


from pyramid.renderers import JSON
from bson import json_util
import json

class MongoJSONRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        request = system.get('request')
        if request is not None:
            # set response type to json
            request.response.content_type = 'application/json; charset=UTF-8'
        return json.dumps(value, default=json_util.default)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    my_session_factory = SignedCookieSessionFactory('itsaseekreet', timeout=None)
    my_authentication_policy = SessionAuthenticationPolicy(callback=groupfinder, debug=False)
    my_authorization_policy = ACLAuthorizationPolicy()
    
    config = Configurator(settings=settings)
    config.set_root_factory(Root)
    config.set_session_factory(my_session_factory)
    config.set_authentication_policy(my_authentication_policy)
    config.set_authorization_policy(my_authorization_policy)

    # add mongo db
    config.add_subscriber(add_mongo_db, NewRequest)
    # add cors headers
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    # add csrf token header
    config.add_subscriber(add_csrf_token_header, NewRequest)

    # override default json renderer
    config.add_renderer('json', MongoJSONRenderer) 

    config.add_route('options', '/*foo', request_method='OPTIONS') # matches any path OPTIONS method
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('auth', '/auth')
    config.add_route('search', '/search')
    config.scan()
    return config.make_wsgi_app()
