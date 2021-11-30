from time import sleep

import requests

from settings import SERVICE_TOKEN, PERSONAL_TOKEN, VERSION, GROUP_IDS, RESTRICTED, HTTP_PROXY, HTTPS_PROXY


class VKParser:

    def __init__(self):
        self.service_token = SERVICE_TOKEN
        self.personal_token = PERSONAL_TOKEN
        self.version = VERSION

        self.group_id = GROUP_IDS
        self.restricted = RESTRICTED

        self.api_url = 'https://api.vk.com/method/'
        self.methods = dict(photos='photos.get?', albums='photos.getAlbums?', comments='photos.getAllComments?')
        self.proxy = dict(http=HTTP_PROXY, https=HTTPS_PROXY)
        self.offset = 0


class AlbumsParser(VKParser):

    def get_albums(self, group_name: str) -> list:
        """
        Собирает id альбомов, в которых есть слово продажа и возвращает списком.

        :param group_name: Принимает название группы из словаря {'название': '-id'}
        :return: Возвращает список id альбомов
        """
        response = requests.get(self.api_url + self.methods.get('albums', None),
                                params={
                                    'access_token': self.personal_token,
                                    'v': VERSION,
                                    'owner_id': self.group_id.get(group_name, None)
                                }, proxies=self.proxy)
        data = response.json()
        return [item.get('id') for item in data.get('response').get('items')
                if 'продажа' in str(item.get('title').lower())  # TODO переписать так, чтобы не было "продажа"
                and str(item.get('title').lower()) not in self.restricted]

    def get_photos(self, group_name: str) -> dict:
        """
        Проходит по всем фотографиям альбома по его id, чтобы собрать ссылки и описания фотографий.

        :param group_name: Принимает название группы из словаря {'название': '-id'}
        :return: Возвращает словарь {picture_id: {'link': link, 'text': text, 'comments': []}
        """
        photos_list = {}
        albums = self.get_albums(group_name)
        for album in albums:
            while True:
                response = requests.get(self.api_url + self.methods.get('photos'),
                                        params={
                                            'access_token': self.personal_token,
                                            'v': VERSION,
                                            'owner_id': self.group_id.get(group_name),
                                            'album_id': album,
                                            'offset': self.offset,
                                            'count': 1000
                                        }, proxies=self.proxy)
                data = response.json()
                for item in data.get('response').get('items'):
                    link = f"https://vk.com/photo{self.group_id.get(group_name)}_{item.get('id')}"
                    text = item.get('text').lower()
                    photos_list[item.get('id')] = {'link': link, 'text': text, 'comments': []}
                self.offset += 100
                sleep(0.1)
                if not data.get('response').get('items'):
                    self.offset = 0
                    break
        return photos_list

    def get_comments(self, group_name: str, all_photos: dict) -> dict:
        """
        Собирает все комментарии альбома по его id

        :param str group_name: Принимает название группы из словаря {'название': '-id'}
        :param all_photos: Принимает словарь, где ключ picture_id, а значение словарь {'link': link, 'text': text,
        'comments': []}
        :return: Возвращает словарь {picture_id: {'link': link, 'text': text, 'comments': [comment1, comment2, ...]}
        """
        albums = self.get_albums(group_name)
        for album in albums:
            while True:
                response = requests.get(self.api_url + self.methods['comments'],
                                        params={
                                            'access_token': self.personal_token,
                                            'v': VERSION,
                                            'owner_id': self.group_id.get(group_name),
                                            'album_id': album,
                                            'offset': self.offset,
                                            'count': 100
                                        }, proxies=self.proxy)
                data = response.json()
                for item in data.get('response').get('items'):
                    text = item.get('text').lower()
                    all_photos[item.get('pid')]['comments'].append(text)
                self.offset += 100
                sleep(0.1)
                if not data.get('response').get('items'):
                    self.offset = 0
                    break
        return all_photos
