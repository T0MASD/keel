from keel.resources import Projects, Project
from pyramid.view import view_config



@view_config(request_method='GET', context=Projects, renderer='json')
def list_projects(context, request):
    r = context.retrieve(spec=None, fields={"name":1, "description":1, "site":1})

    if r is None:
        raise HTTPNotFound()
    else:
        return r


@view_config(request_method='POST', context=Projects, renderer='json')
def create_project(context, request):
    result = context.create(request.json_body)

    return request.json_body


@view_config(request_method='GET', context=Project, renderer='json')
def get_project(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r