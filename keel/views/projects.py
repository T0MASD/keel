from keel.resources import Projects, Project, Teams, Team
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
    result = context.create(request.json_body)

    return request.json_body


@view_config(request_method='GET', context=Project, renderer='json')
def get_project(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r

@view_config(request_method='PATCH', context=Project, renderer='json')
@view_config(request_method='PUT', context=Project, renderer='json')
def update_project(context, request):
    context.update(request.json_body, True)

    return Response(status_int=202)


@view_config(request_method='DELETE', context=Project, renderer='json')
def delete_project(context, request):
    context.delete()

    return Response(status_int=202)


@view_config(request_method='GET', context=Teams, renderer='json')
def list_project_teams(context, request):
    parent_project_id = context.__parent__.__name__
    r = context.retrieve(spec={"project_id":parent_project_id}, fields={"name":1, "people":1})
    return r


@view_config(request_method='GET', context=Team, renderer='json')
def get_project_team(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        # check if team belongs to the project
        parent_project_id = context.__parent__.__parent__.__name__
        if r['project_id'] == parent_project_id:
            return r
        else:
            raise HTTPNotFound()
