
def get_basicauth_credentials(request):
    from paste.httpheaders import AUTHORIZATION    
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


def check_credentials(credentials, settings):
    if credentials != None and set(['username', 'password']) == set(credentials.keys()):
        # DO Login check here
        if settings and 'check_password' in settings and settings['check_password'] == 'true':
            # do the check
            print "checking password!"
            return credentials['username']
        else:
            return credentials['username']