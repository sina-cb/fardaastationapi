# from episodes import Episodes, db
from bs4 import BeautifulSoup
from urlparse import urljoin

import requests
import schedule
import time
import os

from logging import error as logi

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')


def read_from_file():
    with open(os.path.join(APP_STATIC, 'initial_seed.txt')) as f:
        uris = f.readlines()
    uris = [x.strip() for x in uris]
    return uris


def update_episodes(initial_seed=False):
    # # Get the last episodes posted in the webpage.
    # radio_farda_base_url = "https://www.radiofarda.com/"
    # fardaa_station_base_url = urljoin(radio_farda_base_url, "z/20317")
    # page = requests.get(fardaa_station_base_url)
    # episodes = \
    #     BeautifulSoup(page.content, 'html.parser').find_all(id='episodes')[
    #         0].find_all(id='items')[0].find_all('a', class_='img-wrap')
    #
    # # Download the corresponding pages and get the
    # # information for each episode and add to the
    # # database.
    #
    # # If db is empty, read the initial uri's from the initial_seed.txt to
    # # get all the older episodes too.
    # initial_seed = False
    # if len(db) == 0:
    #     initial_seed = True
    #     episodes = read_from_file()
    #
    # timestamp = int(time.time())
    # for base_uri in episodes:
    #     if not initial_seed:
    #         base_uri = base_uri['href']
    #     if not db.contains(where('base_uri') == base_uri):
    #         try:
    #             episode_page = requests.get(
    #                 urljoin(radio_farda_base_url, base_uri))
    #             episode_page = BeautifulSoup(episode_page.content,
    #                                          'html.parser')
    #
    #             image_uri = \
    #                 episode_page.find_all('a', class_='html5PlayerImage')[
    #                     0].find('img')['src']
    #
    #             both_download_links = \
    #                 episode_page.find_all('div', class_='media-download')[
    #                     0].find_all('ul', class_='subitems')[
    #                     0].find_all('li', 'subitem')
    #
    #             low_quality = both_download_links[0].find('a')['href']
    #
    #             high_quality = ''
    #             if len(both_download_links) > 1:
    #                 high_quality = both_download_links[1].find('a')['href']
    #
    #             publish_date = episode_page.find_all('div', 'published')[
    #                 0].find('time').text
    #
    #             title = episode_page.find_all('div', 'hdr-container')[
    #                 0].find('h1').text
    #
    #             db.insert({'timestamp': timestamp,
    #                        'title': title.strip(),
    #                        'date': publish_date.strip(),
    #                        'base_uri': base_uri.strip(),
    #                        'low_quality': low_quality.strip(),
    #                        'high_quality': high_quality.strip(),
    #                        'image_uri': image_uri.strip()
    #                        })
    #         except IndexError:
    #             logi("Index Error at: " + base_uri)
    #         finally:
    #             logi("Fetched: " + base_uri)
    logi("Finished updating.")


def scheduler_thread():
    schedule.every(1).seconds.do(update_episodes)

    while True:
        schedule.run_pending()
