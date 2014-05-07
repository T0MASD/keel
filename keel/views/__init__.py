from keel.resources import Root
from pyramid.view import view_config

@view_config(renderer='json', context=Root)
def home(context, request):
    return {'info': 'Project API'}


@view_config(request_method='OPTIONS')
def handle_options(request):
    ''' this is dummy reponse to OPTIONS method called by ajax, 
    request.response.headers are set in add_cors_headers_response_callback '''
    return request.response