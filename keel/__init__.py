from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'g:manager', 'edit'),
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


def groupfinder(username, request):
    groups = []
    if username == 'adminuser':
        groups.append('admin')
    if username == 'manageruser':
        groups.append('manager')
    return ['g:%s' % g for g in groups]


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    my_authentication_policy = SessionAuthenticationPolicy(callback=groupfinder, debug=False)
    my_authorization_policy = ACLAuthorizationPolicy()
    
    config = Configurator(settings=settings)
    config.set_root_factory(Root)
    config.set_session_factory(my_session_factory)
    config.set_authentication_policy(my_authentication_policy)
    config.set_authorization_policy(my_authorization_policy)

    config.include('cornice')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('auth', '/auth')
    config.scan()
    return config.make_wsgi_app()
