from keel.resources import Teams, Team, Members
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response


@view_config(request_method='GET', context=Teams, renderer='json')
def list_project_teams(context, request):
    parent_project_id = context.__parent__.__name__
    teams = context.retrieve(spec={"project_id":parent_project_id}, fields={"name":1})
    # add members to the teams
    for team in teams:
        # strip ObjectId()
        team_id = str(team['_id'])
        # initialize members collection
        members = Members(ref='', parent=None)
        # add request required for db comms
        members.request = request
        # set members property
        team['members'] = members.retrieve(spec={"team_id":team_id})
    return teams


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