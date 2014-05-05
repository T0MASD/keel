from keel.resources import Cities, Root
from pyramid.view import view_config


@view_config(renderer='json', context=Root)
def home(context, request):
    return {'info': 'City API'}


@view_config(request_method='GET', context=Cities, renderer='json', permission='authenticated')
def list_cities(context, request):
    return context.retrieve()