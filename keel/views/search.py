from pyramid.view import view_config
from keel.resources import Members
from keel.helpers.people import people_lookup


@view_config(route_name='search', renderer='json')
def search(request):
    """ search view """
    if 'resource' not in request.params:
        return []
    if request.params['resource'] == 'memberRoles' and 'query' in request.params:
        # look for member roles
        members = Members(ref='', parent=None)
        members.request = request
        r = members.retrieve(spec={"role":{'$regex': request.params['query'], '$options': 'i' }}, fields={"role":1})
        result = set([member['role'] for member in r])
        return list(result)
    elif request.params['resource'] == 'people' and 'query' in request.params:
        return people_lookup(request.params['query'], request.registry.settings)
    else:
        return []

