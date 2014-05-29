import requests

def people_lookup(search_term, settings):
    r = requests.get('http://api.nobelprize.org/v1/prize.json')
    people = []
    for award in r.json()['prizes']:
        for person in award['laureates']:
            if 'firstname' in person and 'surname' in person:
                if any([search_term.lower() in person['firstname'].lower(), search_term.lower() in person['surname'].lower()]):
                    record = {'personId':person['id'], 'name': '%s %s' % (person['firstname'], person['surname'])}
                    people.append(record)
    return people