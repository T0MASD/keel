from cornice import Service

projects = Service(name='projects', path='/projects', description="Get projects")

@projects.get()
def get_projects(request):
    data = {}
    data['projects'] = ['Project 1', 'Project 2', 'Project 3']
    return data
