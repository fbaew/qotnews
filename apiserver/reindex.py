import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

import database
from sqlalchemy import select
import search
import sys

import time
import json
import requests

database.init()
search.init()

BATCH_SIZE = 5000

def put_stories(stories):
    return search.meili_api(requests.post, 'indexes/qotnews/documents', stories)

def get_update(update_id):
    return search.meili_api(requests.get, 'tasks/{}'.format(update_id))

if __name__ == '__main__':
    num_stories = database.count_stories()

    print('Reindex {} stories?'.format(num_stories))
    print('Press ENTER to continue, ctrl-c to cancel')
    input()

    story_list = database.get_story_list()

    count = 1
    while len(story_list):
        stories = []

        for _ in range(BATCH_SIZE):
            try:
                sid = story_list.pop()
            except IndexError:
                break

            story = database.get_story(sid)
            print('Indexing {}/{} id: {} title: {}'.format(count, num_stories, sid[0], story.title))
            story_obj = json.loads(story.meta_json)
            stories.append(story_obj)
            count += 1

        res = put_stories(stories)
        update_id = res['uid']

        print('Waiting for processing', end='')
        while get_update(update_id)['status'] != 'succeeded':
            time.sleep(0.5)
            print('.', end='', flush=True)

        print()

    print('Done.')

