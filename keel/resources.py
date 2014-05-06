from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated
from pyramid.traversal import find_root
from bson.objectid import ObjectId

class Resource(dict):

    def __init__(self, ref, parent):
        self.__name__ = ref
        self.__parent__ = parent

    def __repr__(self):
        # use standard object representation (not dict's)
        return object.__repr__(self)
        
    def add_child(self, ref, klass):
        resource = klass(ref=ref, parent=self)
        self[ref] = resource


class MongoCollection(Resource):
    ''' mongo db collection '''

    @property
    def collection(self):
        root = find_root(self)
        request = root.request
        return request.db[self.collection_name]

    # get all documents from the collection
    def retrieve(self):
        return [elem for elem in self.collection.find()]

    # add new document to the collection
    def create(self, document):
        object_id = self.collection.insert(document)
        return self.resource_name(ref=str(object_id), parent=self)


class MongoDocument(Resource):
    '''' mongo document '''

    def __init__(self, ref, parent):
        Resource.__init__(self, ref, parent)

        self.collection = parent.collection
        # document identifier
        self.spec = {'_id': ObjectId(ref)}

    # Return document
    def retrieve(self):
        return self.collection.find_one(self.spec)

    # Update document
    def update(self, data, patch=False):
        if patch:
            data = {'$set': data}

        self.collection.update(self.spec, data)

    # Delete document
    def delete(self):
        self.collection.remove(self.spec)


class City(MongoDocument):
    
    def __init__(self, ref, parent):
        MongoDocument.__init__(self, ref, parent)


class Cities(MongoCollection):
    
    collection_name = 'cities'
    resource_name = City

    def __getitem__(self, ref):
        return City(ref, self)


class Root(Resource):
    __acl__ = [
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'g:manager', 'edit'),
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

        Resource.__init__(self, ref='', parent=None)
        self.add_child('cities', Cities)