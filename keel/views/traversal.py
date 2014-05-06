from keel.resources import Cities, City
from pyramid.view import view_config



@view_config(request_method='GET', context=Cities, renderer='json')
def list_cities(context, request):
    return context.retrieve()


@view_config(request_method='POST', context=Cities, renderer='json')
def create_city(context, request):
    result = context.create(request.json_body)

    return request.json_body

@view_config(request_method='GET', context=City, renderer='json')
def get_city(context, request):
    from pprint import pprint
    pprint (vars(context))


    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r