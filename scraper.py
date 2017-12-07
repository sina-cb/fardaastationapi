# from episodes import Episodes, db
from bs4 import BeautifulSoup
from urlparse import urljoin

import requests
import time
import os

from logging import info as logi

from episodes import Episodes, _create_database

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')


def read_from_file():
    with open(os.path.join(APP_STATIC, 'initial_seed.txt')) as f:
        uris = f.readlines()
    uris = [x.strip() for x in uris]
    return uris


def update_episodes(create_db=False):
    # Get the last episodes posted in the webpage.
    radio_farda_base_url = "https://www.radiofarda.com/"
    fardaa_station_base_url = urljoin(radio_farda_base_url, "z/20317")
    page = requests.get(fardaa_station_base_url)
    episodes = \
        BeautifulSoup(page.content, 'html.parser').find_all(id='episodes')[
            0].find_all(id='items')[0].find_all('a', class_='img-wrap')

    if create_db:
        episodes = read_from_file()

    # Download the corresponding pages and get the
    # information for each episode and add to the
    # database.
    timestamp = int(time.time())
    for base_uri in episodes:
        if not create_db:
            base_uri = base_uri['href']

        # Actually try to add the episode to MySQL
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

            import peewee
            try:
                query = Episodes.insert(timestamp=timestamp, title=title.strip(), date=publish_date.strip(),
                                        base_uri=base_uri.strip(), low_quality=low_quality.strip(),
                                        high_quality=high_quality.strip(), image_uri=image_uri.strip())
                query.execute()
            except peewee.IntegrityError:
                logi('Repeated episode.')
        except IndexError:
            logi("Index Error at: " + base_uri)
        finally:
            logi("Fetched: " + base_uri)


if __name__ == '__main__':
    _create_database()
    update_episodes(create_db=True)
