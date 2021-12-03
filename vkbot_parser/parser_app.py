import time

import requests

from vkbot_parser.vk_parser import AlbumsParser

from settings import AUTH_TOKEN

app = AlbumsParser()

if __name__ == '__main__':
    start_time = time.time()
    photos = app.get_photos(group_name='esg')
    photos_and_comments = app.get_comments(group_name='esg', all_photos=photos)

    write_to_db = []
    # TODO удаление из базы
    for value in photos_and_comments.values():
        link = value['link']
        if value['text'] != '':
            try:
                if value['comments'][-1] != '':
                    text = f"Описание фото:\n{value['text']}.\n\n1-ый комментарий к фото:\n" \
                           f"{value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Описание фото:\n{value['text']}".replace(u'\xa0', u'')
            except IndexError as err:
                text = f"Описание фото:\n{value['text']}".replace(u'\xa0', u'')
        else:
            try:
                if value['comments'][-1] != '':
                    text = f"1-ый комментарий к фото:\n{value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Что-то пошло не так. Нет ни описания, ни комментариев ¯\_(ツ)_/¯"
            except IndexError as err:
                text = f"Что-то пошло не так. Нет ни описания, ни комментариев ¯\_(ツ)_/¯"
        write_to_db.append({"link": link, "text": text})
    for item in write_to_db:
        requests.post(url='http://127.0.0.1:8080/add_items/', headers={'auth': AUTH_TOKEN}, json=item)
    print(len(write_to_db))
    print(f'Время выполнения парсинга: {time.time() - start_time} секунд')
