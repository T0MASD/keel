from keel.resources import Projects, Project
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response

@view_config(request_method='GET', context=Projects, renderer='json')
def list_projects(context, request):
    r = context.retrieve(spec=None, fields={"name":1, "description":1, "site":1})

    if r is None:
        raise HTTPNotFound()
    else:
        return r


@view_config(request_method='POST', context=Projects, renderer='json')
def create_project(context, request):
    # parse json
    json_body = request.json_body
    # create project, updates json_body including ObjectId
    context.create(json_body)
    # return updated json body
    return json_body


@view_config(request_method='GET', context=Project, renderer='json')
def get_project(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r

@view_config(request_method='PATCH', context=Project, renderer='json', permission='authenticated')
@view_config(request_method='PUT', context=Project, renderer='json', permission='authenticated')
def update_project(context, request):
    context.update(request.json_body, True)

    return Response(status_int=202)


@view_config(request_method='DELETE', context=Project, renderer='json', permission='edit')
def delete_project(context, request):
    context.delete()

    return Response(status_int=202)




