import logging
import database

import json

database.init()

def fix_gzip_bug(story_list):
    FIX_THRESHOLD = 150

    count = 1
    for sid in story_list:
        try:
            sid = sid[0]
            story = database.get_story(sid)
            full_json = json.loads(story.full_json)
            text = full_json.get('text', '')

            count = text.count('�')
            if not count: continue

            ratio = count / len(text) * 1000
            print('Bad story:', sid, 'Num ?:', count, 'Ratio:', ratio)
        except KeyboardInterrupt:
            raise
        except BaseException as e:
            logging.exception(e)
            breakpoint()

if __name__ == '__main__':
    num_stories = database.count_stories()

    print('Fix {} stories?'.format(num_stories))
    print('Press ENTER to continue, ctrl-c to cancel')
    input()

    story_list = database.get_story_list()

    fix_gzip_bug(story_list)

