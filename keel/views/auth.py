from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
from pyramid.session import check_csrf_token
import pyramid.httpexceptions as exc
from keel.helpers.auth import check_credentials, get_basicauth_credentials


@view_config(route_name='login', renderer='json', request_method='GET')
def login(request):
    """ login view """
    if not request.authenticated_userid:
        credentials = get_basicauth_credentials(request)
        username = check_credentials(credentials, request.registry.settings)
        if username:
            headers = remember(request, username)
            request.response.headerlist.extend(headers)
            request.session.flash('success|Login|You have logged in as %s' % username)
            return {'username':username}
        else:
            request.response.status = 401
            return {
                "toasterStatus": "error",
                "toasterTitle": "Login",
                "toasterMessage": "Failed, please check your password"
                }            
    else:
        username = request.authenticated_userid
        request.session.flash('info|Login|You are already logged in as %s' % username)
        return {'username':username}


@view_config(route_name='logout', renderer='json', request_method='GET')
def logout(request):
    """ logout view """
    if request.authenticated_userid:
        username = request.authenticated_userid
        headers = forget(request)
        request.response.headerlist.extend(headers)
        request.session.flash('success|Logout|Logged out %s' % username)
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
