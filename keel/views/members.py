from keel.resources import Members, Member
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response


@view_config(request_method='GET', context=Members, renderer='json')
def list_team_members(context, request):
    parent_id = context.__parent__.__name__
    r = context.retrieve(spec={"teamId":parent_id})
    return r


@view_config(request_method='GET', context=Member, renderer='json')
def get_team_member(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        # check if member belongs to the team
        parent_id = context.__parent__.__parent__.__name__
        if r['teamId'] == parent_id:
            return r
        else:
            raise HTTPNotFound()


@view_config(request_method='POST', context=Members, renderer='json')
def add_member(context, request):
    # parse json
    json_body = request.json_body
    # create team, returns Team objext
    member = context.create(json_body)
    # update json body to include team id
    json_body.update(member.spec)
    # return updated json body
    return json_body


@view_config(request_method='PATCH', context=Member, renderer='json')
@view_config(request_method='PUT', context=Member, renderer='json')
def update_member(context, request):
    context.update(request.json_body, True)
    json_body = request.json_body
    return Response(status_int=202, json_body=json_body)


@view_config(request_method='DELETE', context=Member, renderer='json')
def delete_member(context, request):
    context.delete()
    
    return Response(status_int=202) 