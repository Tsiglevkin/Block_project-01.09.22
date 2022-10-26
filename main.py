from VK import VK

with open('token.txt', encoding='utf-8') as f:
    vk_token = f.readline()

if __name__ == "__main__":

    access_token = vk_token
    user_id = '607170157'

    vk = VK(access_token, user_id)
    vk.send_all('For course project/photo_JSON')
