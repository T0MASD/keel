from keel.resources import Root
from pyramid.view import view_config

@view_config(renderer='json', context=Root)
def home(context, request):
    return {'info': 'Project API'}