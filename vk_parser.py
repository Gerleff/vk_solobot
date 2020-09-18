"""
:authors: gerleffx2
:license:
:copyright: (c) 2019 gerleffx2
"""

import random
from config import user_token, photo_min
from data import posts_amount
import requests
import bs4

token = user_token
version = 5.103
domain = 'jpeg_pictures'


def post_get():
    offset = random.randint(0, posts_amount)
    response = requests.get('https://api.vk.com/method/wall.get', params=dict(access_token=token, v=version,
                                                                              domain=domain, count=1, offset=offset))
    return response.json()['response']['items'][0]['id']

def photos_amount_parse():
    html = requests.get('https://vk.com/albums-112199313', headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; '
                                                                                  'WOW64) AppleWebKit/537.36 (KHTML, '
                                                                                  'like Gecko) Chrome/78.0.3904.97 '
                                                                                  'Safari/537.36'})
    soup = bs4.BeautifulSoup(html.text, features="html.parser")
    alb_names = soup.find_all('div', class_='photos_album_title ge_photos_album')
    for title in alb_names:
        if title['title'] == 'Make kartinochki great again!':
            order = alb_names.index(title)
    photos_count = soup.find_all('div', class_='photos_album_counter fl_r')
    result = []
    for ch in photos_count[order]:
        try:
            result.append(int(ch))
        except:
            continue
    return result[0]

def data_collect():
    posts_amount = requests.get('https://api.vk.com/method/wall.get', params=dict(access_token=token, v=version,
                                                                                  domain=domain, count=1, offset=0))
    photos_amount = photos_amount_parse()
    photo_max = int(photo_min) + photos_amount - 1
    posts_amount = posts_amount.json()['response']['count']


    with open('data.py', 'w') as f:
        f.write('photo_max , posts_amount, photos_amount= {}, {}, {}'.format(photo_max, posts_amount, photos_amount))
        f.close()


def main():
    data_collect()
    print('Collected')

if __name__ == "__main__":
    main()
