import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

import requests
import time
from bs4 import BeautifulSoup

import settings
from feeds import hackernews, reddit, tildes, manual, lobsters

INVALID_DOMAINS = ['youtube.com', 'bloomberg.com', 'wsj.com', 'sec.gov']
TWO_DAYS = 60*60*24*2

def list():
    feed = []
    if settings.NUM_HACKERNEWS:
        feed += [(x, 'hackernews') for x in hackernews.feed()[:settings.NUM_HACKERNEWS]]

    if settings.NUM_LOBSTERS:
        feed += [(x, 'lobsters') for x in lobsters.feed()[:settings.NUM_LOBSTERS]]

    if settings.NUM_REDDIT:
        feed += [(x, 'reddit') for x in reddit.feed()[:settings.NUM_REDDIT]]

    if settings.NUM_TILDES:
        feed += [(x, 'tildes') for x in tildes.feed()[:settings.NUM_TILDES]]

    return feed

def get_article(url):
    if not settings.READER_URL:
        logging.info('Readerserver not configured, aborting.')
        return ''

    try:
        r = requests.post(settings.READER_URL, data=dict(url=url), timeout=20)
        if r.status_code != 200:
            raise Exception('Bad response code ' + str(r.status_code))
        return r.text
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        logging.error('Problem getting article: {}'.format(str(e)))
        return ''

def get_content_type(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
        return requests.get(url, headers=headers, timeout=5).headers['content-type']
    except:
        return ''

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'X-Forwarded-For': '66.249.66.1',
        }
        return requests.get(url, headers=headers, timeout=10).headers['content-type']
    except:
        pass

def update_story(story, is_manual=False):
    res = {}

    if story['source'] == 'hackernews':
        res = hackernews.story(story['ref'])
    elif story['source'] == 'lobsters':
        res = lobsters.story(story['ref'])
    elif story['source'] == 'reddit':
        res = reddit.story(story['ref'])
    elif story['source'] == 'tildes':
        res = tildes.story(story['ref'])
    elif story['source'] == 'manual':
        res = manual.story(story['ref'])

    if res:
        story.update(res) # join dicts
    else:
        logging.info('Story not ready yet')
        return False

    if story['date'] and not is_manual and story['date'] + TWO_DAYS < time.time():
        logging.info('Story too old, removing')
        return False

    if story.get('url', '') and not story.get('text', ''):
        if not get_content_type(story['url']).startswith('text/'):
            logging.info('URL invalid file type / content type:')
            logging.info(story['url'])
            return False

        if any([domain in story['url'] for domain in INVALID_DOMAINS]):
            logging.info('URL invalid domain:')
            logging.info(story['url'])
            return False

        logging.info('Getting article ' + story['url'])
        story['text'] = get_article(story['url'])
        if not story['text']: return False

    return True

if __name__ == '__main__':
    #test_news_cache = {}
    #nid = 'jean'
    #ref = 20802050
    #source = 'hackernews'
    #test_news_cache[nid] = dict(id=nid, ref=ref, source=source)
    #news_story = test_news_cache[nid]
    #update_story(news_story)

    #print(get_article('https://www.bloomberg.com/news/articles/2019-09-23/xi-s-communists-under-pressure-as-high-prices-hit-china-workers'))

    a = get_content_type('https://tefkos.comminfo.rutgers.edu/Courses/e530/Readings/Beal%202008%20full%20text%20searching.pdf')
    print(a)

    print('done')
