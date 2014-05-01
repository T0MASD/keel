from cornice import Service
from pyramid.session import check_csrf_token

projects = Service(name='projects', path='/projects', description="Get projects")

def valid_token(request):
    """ checks for a GET or POST parameter named csrf_token or a header named X-CSRF-Token. """
    check_csrf_token(request)


@projects.get(permission="query", validators=valid_token)
def get_projects(request):
    data = {}
    data['projects'] = ['Project 1', 'Project 2', 'Project 3']
    return data
