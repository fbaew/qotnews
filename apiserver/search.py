import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

import requests

MEILI_URL = 'http://127.0.0.1:7700/'

def meili_api(method, route, json=None, params=None):
    try:
        r = method(MEILI_URL + route, json=json, params=params, timeout=4)
        if r.status_code > 299:
            raise Exception('Bad response code ' + str(r.status_code))
        return r.json()
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        logging.error('Problem with MeiliSearch api route: %s: %s', route, str(e))
        return False

def create_index():
    json = dict(uid='qotnews', primaryKey='id')
    return meili_api(requests.post, 'indexes', json=json)

def update_rankings():
    json = ['typo', 'words', 'proximity', 'date:desc', 'exactness']
    return meili_api(requests.post, 'indexes/qotnews/settings/ranking-rules', json=json)

def update_attributes():
    json = ['title']
    r = meili_api(requests.post, 'indexes/qotnews/settings/searchable-attributes', json=json)
    json = ['id']
    r = meili_api(requests.post, 'indexes/qotnews/settings/displayed-attributes', json=json)
    return r

def init():
    print(create_index())
    update_rankings()
    update_attributes()

def put_story(story):
    to_add = dict(title=story['title'], id=story['id'], date=story['date'])
    return meili_api(requests.post, 'indexes/qotnews/documents', [to_add])

def search(q):
    params = dict(q=q, limit=250)
    r = meili_api(requests.get, 'indexes/qotnews/search', params=params)
    return r['hits']
    
if __name__ == '__main__':
    init()

    print(update_rankings())

    print(search('qot'))
