import json
import logging

import feed
import database
import search

database.init()

def fix_gzip_bug(story_list):
    FIX_THRESHOLD = 150

    count = 1
    for sid in story_list:
        try:
            sid = sid[0]
            story = database.get_story(sid)
            full_json = json.loads(story.full_json)
            meta_json = json.loads(story.meta_json)
            text = full_json.get('text', '')

            count = text.count('�')
            if not count: continue

            ratio = count / len(text) * 1000
            print('Bad story:', sid, 'Num ?:', count, 'Ratio:', ratio)
            if ratio < FIX_THRESHOLD: continue

            print('Attempting to fix...')

            valid = feed.update_story(meta_json, is_manual=True)
            if valid:
                database.put_story(meta_json)
                search.put_story(meta_json)
                print('Success')
            else:
                print('Story was not valid')

            time.sleep(3)

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

