from keel.resources import Projects, Project
from pyramid.view import view_config



@view_config(context=Projects, request_method='GET', renderer='json')
def list_projects(context, request):
    r = context.retrieve()
    print r
    return r


@view_config(request_method='POST', context=Projects, renderer='json')
def create_city(context, request):
    result = context.create(request.json_body)

    return request.json_body


@view_config(request_method='GET', context=Project, renderer='json')
def get_city(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r