from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
from pyramid.session import check_csrf_token
from paste.httpheaders import AUTHORIZATION
import pyramid.httpexceptions as exc


def get_basicauth_credentials(request):
    authorization = AUTHORIZATION(request.environ)
    try:
        authmeth, auth = authorization.split(' ', 1)
    except ValueError:  # not enough values to unpack
        return None
    if authmeth.lower() == 'basic':
        try:
            auth = auth.strip().decode('base64')
        except binascii.Error:  # can't decode
            return None
        try:
            username, password = auth.split(':', 1)
        except ValueError:  # not enough values to unpack
            return None
        return {'username': username, 'password': password}

    return None


def check_credentials(credentials):
    if credentials != None and set(['username', 'password']) == set(credentials.keys()):
        # DO Login check here
        return credentials['username']


@view_config(route_name='login', renderer='json', request_method='GET')
def login(request):
    """ login view """
    if not request.authenticated_userid:
        credentials = get_basicauth_credentials(request)
        username = check_credentials(credentials)
        if username:
            headers = remember(request, username)
            request.response.headerlist.extend(headers)
            return {'username':username}
        else:
            raise exc.HTTPUnauthorized
    else:
        username = request.authenticated_userid
        return {'username':username}
    


@view_config(route_name='logout', renderer='json', request_method='GET')
def logout(request):
    """ logout view """
    if request.authenticated_userid:
        username = request.authenticated_userid
        headers = forget(request)
        request.response.headerlist.extend(headers)
        return {'status':'Logged out %s' % username}
    else:
        request.response.status = 401
        return {
            "toasterStatus": "warning",
            "toasterTitle": "Warning",
            "toasterMessage": "You are not logged in"
            }


@view_config(route_name='auth', renderer='string')
def auth(request):
    """ auth debug view """
    print 'expecting csrf_token', request.session.get_csrf_token()
    #check_csrf_token(request)
    print request.authenticated_userid
    print request.effective_principals
    token = request.session.new_csrf_token()
    print 'setting new csrf_token', token
    return 'See console'


@forbidden_view_config(renderer='json')
def http_403_unauthenticated(request):
    request.response.status = 403
    return {
        "toasterStatus": "error",
        "toasterTitle": "Forbidden",
        "toasterMessage": "You don't have access to this resource"
        }
