import requests
from tqdm import tqdm
from pprint import pprint


class YandexDisk:
    def __init__(self, token, link='https://cloud-api.yandex.net/v1/disk/resources/upload'):
        self.token = token
        self.link = link

    def get_headers(self):
        return {'Content_Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def _get_upload_link(self, yadisk_file_path):
        """This function can get upload link from Yandex Disk"""
        upload_url = self.link
        headers = self.get_headers()
        parameters = {'path': yadisk_file_path, 'overwrite': 'True'}  # параметры запроса для определения пути файла и
        # и его перезаписи в случае, если он там уже есть. Параметры берутся из документации API.
        response = requests.get(upload_url, headers=headers, params=parameters)  # запрос с заголовками для авторизации
        # и параметрами.
        pprint(f'Получение ссылки для загрузки: {response.status_code}')
        return response.json()  # возврат ссылки в виде словаря JSON.

    def upload_file_to_disc(self, yadisk_file_path, file_name='photos.json'):
        """This function can upload a chosen file to yandex disk"""
        upload_link = self._get_upload_link(yadisk_file_path)  # получаем ссылку в виде json
        href = upload_link.get('href', '')  # получаем обяз. параметр href для метода put, что ниже)
        # headers = self.get_headers()
        response = requests.put(href, data=open(file_name, 'rb'))  # делаем запрос, указываем href и
        # переменную/открытый файл -
        # - в режиме чтения в байтовом виде (позволит отправить любой вид данных).
        pprint(f'Отправка: {response.status_code}')

    def upload_photo(self, some_json):
        """This function uploads photo from some json-file to YandexDisk"""
        url = self.link
        headers = self.get_headers()

        photo_list = some_json
        for item in tqdm(photo_list, desc='Отправляем фото на ЯДиск', unit=' фото'):
            response = requests.post(
                url=url,
                headers=headers,
                params={'path': f"For course project/{item['file_name']}", 'url': item['link']}
            )
            response.raise_for_status()
            if response.status_code == 202:
                print('success')
