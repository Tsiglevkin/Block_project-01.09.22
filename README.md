# Программа для отправки фото пользователя VK в Яндекс Диск.

Эта программа позволяет отправить фото пользователя VK в Яндекс Диск. Сейчас настроена отправка фото профиля, 
для смены требуется в функции get_photos_dict сменить параметр 'album_id' с 'profile' на 'wall' например.
Программа работает не до конца корректно - при получении статусов 202 по всем скаченным и отправленным фото 
на яндекс диск приходит меньше фотографии на несколько штук. Смена ID пользователя не помогла, смена параметра album_id
не помогла. Также в программе не работает модуль progress.bar. Пришлось использовать модуль tqdm.
В остальном программа работает.