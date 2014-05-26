from pyramid.view import view_config
from keel.resources import Members

@view_config(route_name='search', renderer='json')
def search(request):
    """ search view """
    if request.params['resource'] == 'memberRoles' and 'query' in request.params:
        # look for member roles
        members = Members(ref='', parent=None)
        members.request = request
        r = members.retrieve(spec={"role":{'$regex': request.params['query'], '$options': 'i' }}, fields={"role":1})
        result = set([member['role'] for member in r])
        return list(result)
