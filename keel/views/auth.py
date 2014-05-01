from pyramid.security import remember, forget
from pyramid.view import view_config


@view_config(route_name='login', renderer='json')
def login(request):
    """ login view """
    username = 'manageruser'
    headers = remember(request, username)
    request.response.headerlist.extend(headers)
    return {'status':'Logged in %s' % username}


@view_config(route_name='logout', renderer='json')
def logout(request):
    """ logout view """
    username = request.authenticated_userid
    headers = forget(request)
    request.response.headerlist.extend(headers)
    return {'status':'Logged out %s' % username}


@view_config(route_name='auth', renderer='string')
def auth(request):
    """ auth debug view """
    print request.authenticated_userid
    print request.effective_principals
    return 'See console'