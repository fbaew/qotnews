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
    json = ['typo', 'words', 'proximity', 'attribute', 'desc(date)', 'wordsPosition', 'exactness']
    return meili_api(requests.post, 'indexes/qotnews/settings/ranking-rules', json=json)

def update_attributes():
    json = ['title', 'url', 'author', 'link', 'id']
    r = meili_api(requests.post, 'indexes/qotnews/settings/searchable-attributes', json=json)
    meili_api(requests.delete, 'indexes/qotnews/settings/displayed-attributes', json=json)
    return r

def init():
    print(create_index())
    update_rankings()
    update_attributes()

def put_story(story):
    story = story.copy()
    story.pop('text', None)
    story.pop('comments', None)
    return meili_api(requests.post, 'indexes/qotnews/documents', [story])

def search(q):
    params = dict(q=q, limit=250)
    r = meili_api(requests.get, 'indexes/qotnews/search', params=params)
    return r['hits']
    
if __name__ == '__main__':
    init()

    print(search('qot'))
