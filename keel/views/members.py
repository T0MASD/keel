from keel.resources import Members, Member, Persons
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
    # create member, updates json_body including ObjectId
    context.create(json_body)
    # add/update persons entry
    persons = Persons(ref='', parent=None)
    persons.request = request
    person = persons.retrieve(spec={"personId":json_body['personId']})
    if person:
        # person already in persons collection, let's skip
        pass
    else:
        new_person = {"name":json_body['name'], "personId":json_body['personId']}
        persons.create(new_person)
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