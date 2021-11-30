import time

from vkbot_parser.vk_parser import AlbumsParser

app = AlbumsParser()

if __name__ == '__main__':
    start_time = time.time()
    photos = app.get_photos(group_name='esg')
    photos_and_comments = app.get_comments(group_name='esg', all_photos=photos)

    write_to_db = []

    for value in photos_and_comments.values():
        link = value['link']
        if value['text'] != '':
            try:
                if value['comments'][-1] != '':
                    text = f"Описание фото: {value['text']}.\n\n1-ый комментарий к фото: " \
                           f"{value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Описание фото: {value['text']}".replace(u'\xa0', u'')
            except IndexError as err:
                continue
        else:
            try:
                if value['comments'][-1] != '':
                    text = f"1-ый комментарий к фото: {value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Что-то пошло не так. Нет ни описания, ни комментариев ¯\_(ツ)_/¯"
            except IndexError as err:
                continue
        write_to_db.append((link, text))

    print(write_to_db)

    print(f'Время выполнения парсинга: {time.time() - start_time} секунд')
