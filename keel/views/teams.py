from keel.resources import Teams, Team
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response


@view_config(request_method='GET', context=Teams, renderer='json')
def list_project_teams(context, request):
    parent_project_id = context.__parent__.__name__
    r = context.retrieve(spec={"projectId":parent_project_id}, fields={"name":1, "size":1})
    return r


@view_config(request_method='GET', context=Team, renderer='json')
def get_project_team(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        # check if team belongs to the project
        parent_project_id = context.__parent__.__parent__.__name__
        if r['projectId'] == parent_project_id:
            return r
        else:
            raise HTTPNotFound()


@view_config(request_method='POST', context=Teams, renderer='json')
def create_team(context, request):
    # parse json
    json_body = request.json_body
    # create team, updates json_body including ObjectId
    context.create(json_body)
    # return updated json body
    return json_body
    

@view_config(request_method='PATCH', context=Team, renderer='json')
@view_config(request_method='PUT', context=Team, renderer='json')
def update_team(context, request):
    # parse json
    json_body = request.json_body
    context.update(json_body, True)

    return Response(status_int=202, json_body=json_body)


@view_config(request_method='DELETE', context=Team, renderer='json')
def delete_team(context, request):
    context.delete()
    
    return Response(status_int=202)    