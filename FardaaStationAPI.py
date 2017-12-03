import os
import time
from logging import warn as logi
from threading import Thread, Lock
from urlparse import urljoin

import requests
import schedule
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
from flask import request
from tinydb import TinyDB, where

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
mutex = Lock()


def mock_data(db):
    db.purge()
    db.insert({'timestamp': 10,
               'title': 'episode 1',
               'date': 'Azar 1 1392',
               'base_uri': '/a/28803003.html',
               'low_quality': 'download_l/a/28803003.html',
               'high_quality': 'download_h/a/28803003.html',
               'image_uri': 'image/a/28803003.html'
               })
    db.insert({'timestamp': 10,
               'title': 'episode 2',
               'date': 'Azar 1 1392',
               'base_uri': '/a/28803018.html',
               'low_quality': 'download_l/a/28803018.html',
               'high_quality': 'download_h/a/28803018.html',
               'image_uri': 'image/a/28803018.html'
               })
    db.insert({'timestamp': 20,
               'title': 'episode 3',
               'date': 'Aban 1 1392',
               'base_uri': '/a/28803030.html',
               'low_quality': 'download_l/a/28803030.html',
               'high_quality': 'download_h/a/28803030.html',
               'image_uri': 'image/a/28803030.html'
               })


def get_db():
    db = TinyDB(os.path.join(APP_STATIC, 'episodes.json'))
    # mock_data(db)
    return db


def query_db(db, timestamp):
    result = db.search(where('timestamp') > timestamp)
    return result


@app.route('/update')
def get_updates_from_timestamp():
    timestamp = request.args.get('timestamp', '')
    if timestamp == '':
        timestamp = 0
    else:
        timestamp = long(timestamp)

    mutex.acquire()
    db = get_db()
    result = query_db(db, timestamp)
    mutex.release()

    return jsonify(result)


def read_from_file():
    with open(os.path.join(APP_STATIC, 'initial_seed.txt')) as f:
        uris = f.readlines()
    uris = [x.strip() for x in uris]
    return uris


def update_episodes(initial_seed=False):
    # Get the last episodes posted in the webpage.
    radio_farda_base_url = "https://www.radiofarda.com/"
    fardaa_station_base_url = urljoin(radio_farda_base_url, "z/20317")
    page = requests.get(fardaa_station_base_url)
    episodes = \
        BeautifulSoup(page.content, 'html.parser').find_all(id='episodes')[
            0].find_all(id='items')[0].find_all('a', class_='img-wrap')

    # Download the corresponding pages and get the
    # information for each episode and add to the
    # database.
    mutex.acquire()
    db = get_db()

    # If db is empty, read the initial uri's from the initial_seed.txt to
    # get all the older episodes too.
    initial_seed = False
    if len(db) == 0:
        initial_seed = True
        episodes = read_from_file()

    timestamp = int(time.time())
    for base_uri in episodes:
        if not initial_seed:
            base_uri = base_uri['href']
        if not db.contains(where('base_uri') == base_uri):
            try:
                episode_page = requests.get(
                    urljoin(radio_farda_base_url, base_uri))
                episode_page = BeautifulSoup(episode_page.content,
                                             'html.parser')

                image_uri = \
                    episode_page.find_all('a', class_='html5PlayerImage')[
                        0].find('img')['src']

                both_download_links = \
                    episode_page.find_all('div', class_='media-download')[
                        0].find_all('ul', class_='subitems')[
                        0].find_all('li', 'subitem')

                low_quality = both_download_links[0].find('a')['href']

                high_quality = ''
                if len(both_download_links) > 1:
                    high_quality = both_download_links[1].find('a')['href']

                publish_date = episode_page.find_all('div', 'published')[
                    0].find('time').text

                title = episode_page.find_all('div', 'hdr-container')[
                    0].find('h1').text

                db.insert({'timestamp': timestamp,
                           'title': title.strip(),
                           'date': publish_date.strip(),
                           'base_uri': base_uri.strip(),
                           'low_quality': low_quality.strip(),
                           'high_quality': high_quality.strip(),
                           'image_uri': image_uri.strip()
                           })
            except IndexError:
                logi("Index Error at: " + base_uri)
            finally:
                logi("Fetched: " + base_uri)
    mutex.release()
    logi("Finished updating.")


def scheduler_thread():
    schedule.every(1).seconds.do(update_episodes)

    while True:
        schedule.run_pending()


def flask_thread():
    app.run(debug=False)


if __name__ == '__main__':
    flask = Thread(target=flask_thread, args=())
    scheduler = Thread(target=scheduler_thread, args=())

    flask.start()
    scheduler.start()
