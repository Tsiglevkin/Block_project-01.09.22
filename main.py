from VK.VK import VK
import configparser
from pprint import pprint


c = configparser.ConfigParser()
c.read('settings.ini')
vk_token = c['VK']['vk_token']


if __name__ == "__main__":
    user_id = '607170157'

    vk = VK(vk_token, user_id)
    vk.send_all('For course project/photo_JSON')

