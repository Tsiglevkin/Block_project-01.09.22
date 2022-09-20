import json

import requests
from pprint import pprint

from datetime import datetime

with open('token.txt', encoding='utf-8') as file:
    TOKEN = file.readline()

with open('OAuth_token.txt', encoding='utf-8') as f:
    yandex_token = f.readline()


class VK:
    def __init__(self, some_user_token, some_user_id, version='5.131'):
        self.token = some_user_token
        self.id = some_user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos_dict(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'wall',
            'rev': 0,
            'extended': 1,
            }
        response = requests.get(url, params={**self.params, **params})
        return response.json()


def convert_time(some_time):
    timestamp = int(some_time)
    res = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return res


def get_max_photo_list():  # узнать как сделать метод из этой функции.
    result = vk.get_photos_dict()
    max_photo_list = []
    for item in result['response']['items']:
        photo_dict = {'file_name': f"{item['likes']['count']}.jpg"}
        links_dict = {}
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
                max_photo_list[i].setdefault('date', f"{convert_time(item['date'])}")

    return max_photo_list


def get_send_list():
    var = get_max_photo_list()
    for item in var:
        del item['link']
    return var


def get_json_file(some_list):
    with open('photos.json', 'w') as res:
        json.dump(some_list, res, indent=4)
        print('Файл записан.')


# часть с Яндекс Диском.


def get_upload_link(yadisk_file_path):
    """This function can get upload link from Yandex Disk"""
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Content_Type': 'application/json', 'Authorization': f'OAuth {yandex_token}'}
    parameters = {'path': yadisk_file_path, 'overwrite': 'True'}  # параметры запроса для определения пути файла и
    # и его перезаписи в случае, если он там уже есть. Параметры берутся из документации API.
    response = requests.get(upload_url, headers=headers, params=parameters)  # запрос с заголовками для авторизации
    # и параметрами.
    pprint(f'Ссылка: {response.status_code}')
    return response.json()  # возврат ссылки в виде словаря JSON.


def upload_file_to_disc(yadisk_file_path, file_name):
    """This function can upload chosen file to yandex disk"""
    upload_link = get_upload_link(yadisk_file_path=yadisk_file_path)  # получаем ссылку в виде json
    href = upload_link.get('href', '')  # получаем обяз. параметр href для метода put, что ниже)
    response = requests.put(href, data=open(file_name, 'rb'))  # делаем запрос, указываем href и
    # переменную/открытый файл -
    # - в режиме чтения в байтовом виде (позволит отправить любой вид данных).
    pprint(f'Отправка: {response.status_code}')


def upload_photo():
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Content_Type': 'application/json',
               'Authorization': f'OAuth {yandex_token}'}

    photo_list = get_max_photo_list()
    # pprint(photo_list)
    for item in photo_list:
        response = requests.post(
            url=url,
            headers=headers,
            params={'path': f"For course project/{item['file_name']}", 'url': item['link']}
        )
        response.raise_for_status()
        if response.status_code == 202:
            print('success')


if __name__ == "__main__":

    access_token = TOKEN
    user_id = '607170157'

    vk = VK(access_token, user_id)
    # photos_1 = vk.get_photos_dict()
    # pprint(photos_1)

    photos = get_max_photo_list()
    pprint(photos)

    # json_ = get_send_list()
    # pprint(json_)

    # get_json_file(json_)

    # upload_file_to_disc(f"For course project/photo_JSON", 'photos.json')
    # upload_photo()


