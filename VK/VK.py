import json
import requests
from datetime import datetime
from tqdm import tqdm
from Yandex.yandex import YandexDisk
import configparser


c = configparser.ConfigParser()
c.read('settings.ini')
disk = YandexDisk(c['Yandex']['yandex_token'])


class VK:
    def __init__(self, some_user_token, some_user_id, version='5.131'):
        self.token = some_user_token
        self.id = some_user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos_dict(self):
        """This function gets json dict from VK"""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'wall',
            'rev': 0,
            'extended': 1,
            }
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def _convert_time(self, some_time):
        """This function converts date to comfortable view"""
        timestamp = int(some_time)
        res = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return res

    def get_max_photo_list(self):
        """This function make a list with max size photo and append date, if it's photo's duplicate """
        result = self.get_photos_dict()
        max_photo_list = []
        for item in tqdm(result['response']['items'], desc='Скачиваем фото', unit=' фото'):
            photo_dict = {'file_name': f"{item['likes']['count']}.jpg"}
            the_biggest = 0
            for photo_size in item['sizes']:
                if photo_size['height'] > the_biggest:
                    the_biggest = photo_size['height']
                    photo_dict['size'] = photo_size['type']
                    photo_dict['link'] = photo_size['url']
            max_photo_list.append(photo_dict)

            for i in range(len(max_photo_list)):
                counter = 0
                for j in range(len(max_photo_list)):
                    if max_photo_list[i]['file_name'] == max_photo_list[j]['file_name']:
                        counter += 1
                if counter > 1:
                    res = self._convert_time(item['date'])
                    max_photo_list[i].setdefault('date', f"{res}")

        return max_photo_list

    def get_send_list(self):
        """This function makes list for recording in a txt file"""
        var = self.get_max_photo_list()
        for item in var:
            del item['link']
        return var

    def _get_json_file(self):
        """This function records list in a file"""
        with open('../photos.json', 'w') as res:
            json.dump(self.get_send_list(), res, indent=4)

    def _send_json(self, file_path):
        """This function send json to YandexDisk"""
        self._get_json_file()
        disk.upload_file_to_disc(file_path)

    def _send_photo(self):
        """This function send photo from VK to YandexDisk"""
        photo_list = self.get_max_photo_list()
        disk.upload_photo(photo_list)

    def send_all(self, yadisk_file_path):
        """This function send json file and photo from VK to YandexDisk"""
        self._send_json(yadisk_file_path)
        self._send_photo()



