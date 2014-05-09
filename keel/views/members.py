from keel.resources import Members, Member
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response


@view_config(request_method='GET', context=Members, renderer='json')
def list_team_members(context, request):
    parent_id = context.__parent__.__name__
    r = context.retrieve(spec={"team_id":parent_id})
    return r


@view_config(request_method='GET', context=Member, renderer='json')
def get_team_member(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        # check if member belongs to the team
        parent_id = context.__parent__.__parent__.__name__
        if r['team_id'] == parent_id:
            return r
        else:
            raise HTTPNotFound()