import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

import database
from sqlalchemy import select
import search
import sys

import json
import requests

database.init()
search.init()

def count_stories():
    try:
        session = database.Session()
        return session.query(database.Story).count()
    finally:
        session.close()

def get_story_list():
    try:
        session = database.Session()
        return session.query(database.Story.sid).all()
    finally:
        session.close()

if __name__ == '__main__':
    num_stories = count_stories()

    print('Reindex {} stories?'.format(num_stories))
    print('Press ENTER to continue, ctrl-c to cancel')
    input()

    count = 1
    for sid in get_story_list():
        story = database.get_story(sid)
        print('Indexing {}/{} id: {} title: {}'.format(count, num_stories, sid[0], story.title))
        story_obj = json.loads(story.meta_json)
        search.put_story(story_obj)
        count += 1

