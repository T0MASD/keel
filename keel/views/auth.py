from pyramid.security import remember, forget
from pyramid.view import view_config
from pyramid.session import check_csrf_token


@view_config(route_name='login', renderer='json')
def login(request):
    """ login view """
    username = 'manageruser'
    headers = remember(request, username)
    request.response.headerlist.extend(headers)
    csrf_token = request.session.new_csrf_token()
    return {'username':username,
            'csrf_token':csrf_token}


@view_config(route_name='logout', permission='authenticated', renderer='json')
def logout(request):
    """ logout view """
    username = request.authenticated_userid
    headers = forget(request)
    request.response.headerlist.extend(headers)
    return {'status':'Logged out %s' % username}


@view_config(route_name='auth', renderer='string')
def auth(request):
    """ auth debug view """
    print 'expecting csrf_token', request.session.get_csrf_token()
    check_csrf_token(request)
    print request.authenticated_userid
    print request.effective_principals
    token = request.session.new_csrf_token()
    print 'setting new csrf_token', token
    return 'See console'