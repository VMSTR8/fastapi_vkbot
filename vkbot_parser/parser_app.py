import logging
import time
from datetime import datetime

import requests
from sqlalchemy.exc import OperationalError

from vk_parser import AlbumsParser

from vkbot_sql.crud import delete_all_items
from get_db import get_db

from settings.settings import AUTH_TOKEN

log_date = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M')
logging.basicConfig(level=logging.INFO,
                    filename=f'/var/log/bot/{log_date}_parser_app.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s')

app = AlbumsParser()


def main():
    start_time = time.time()

    try:
        photos = app.get_photos(group_name='esg')
        photos_and_comments = app.get_comments(group_name='esg', all_photos=photos)
    except Exception as err:
        logging.error(f'{err} - данные не были собраны')
        time.sleep(300)
        return main()

    try:
        delete_all_items(next(get_db()))
    except OperationalError:
        logging.critical('Что-то не так с базой, не получилось приконектиться')

    write_to_db = []

    for value in photos_and_comments.values():
        link = value['link']
        if value['text'] != '':
            try:
                if value['comments'][-1] != '':
                    text = f"Описание фото:\n{value['text']}.\n\n1-ый комментарий к фото:\n" \
                           f"{value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Описание фото:\n{value['text']}".replace(u'\xa0', u'')
            except IndexError:
                text = f"Описание фото:\n{value['text']}".replace(u'\xa0', u'')
        else:
            try:
                if value['comments'][-1] != '':
                    text = f"1-ый комментарий к фото:\n{value['comments'][-1]}".replace(u'\xa0', u'')
                else:
                    text = f"Что-то пошло не так. Нет ни описания, ни комментариев ¯\_(ツ)_/¯"
            except IndexError:
                text = f"Что-то пошло не так. Нет ни описания, ни комментариев ¯\_(ツ)_/¯"
        write_to_db.append({"link": link, "text": text})

    try:
        requests.post(url='http://127.0.0.1/add_items/', headers={'auth': AUTH_TOKEN}, json=write_to_db)
    except Exception as err:
        logging.critical(f'{err} - не удалось записать в базу')

    logging.info(f'Вхождений в базу: {len(write_to_db)}')
    logging.info(f'Время выполнения парсинга: {time.time() - start_time} секунд')


if __name__ == '__main__':
    main()
