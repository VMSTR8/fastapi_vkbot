import json

from vkbot_sql.crud import get_answer

from answers import *

with open('./keyboards/start_bot.json', 'r', encoding='utf-8') as start_bot, \
        open('./keyboards/main_keyboard.json', 'r', encoding='utf-8') as main_keyboard, \
        open('./keyboards/start_menu.json', 'r', encoding='utf-8') as start_menu, \
        open('./keyboards/faq_keyboard.json', 'r', encoding='utf-8') as faq_keyboard, \
        open('./keyboards/categories_keyboard.json', 'r', encoding='utf-8') as categories_keyboard, \
        open('./keyboards/kitlist.json', 'r', encoding='utf-8') as kitlist, \
        open('./keyboards/orq_questions.json', 'r', encoding='utf-8') as orq_questions, \
        open('./keyboards/media_keyboard.json', 'r', encoding='utf-8') as media_keyboard, \
        open('./keyboards/about_team_keyboard.json', 'r', encoding='utf-8') as about_team_keyboard, \
        open('./keyboards/bonus_keyboard.json', 'r', encoding='utf-8') as bonus_keyboard, \
        open('./keyboards/other_questions_keyboard.json', 'r', encoding='utf-8') as other_questions_keyboard:
    start = json.dumps(json.load(start_bot))
    mk = json.dumps(json.load(main_keyboard))
    st = json.dumps(json.load(start_menu))
    fq = json.dumps(json.load(faq_keyboard))
    ck = json.dumps(json.load(categories_keyboard))
    kitlist_q = json.dumps(json.load(kitlist))
    org_q = json.dumps(json.load(orq_questions))
    media_q = json.dumps(json.load(media_keyboard))
    team_q = json.dumps(json.load(about_team_keyboard))
    bonus_q = json.dumps(json.load(bonus_keyboard))
    other_q = json.dumps(json.load(other_questions_keyboard))

button = {
    '1': [FAQ_1],
    '2': [FAQ_2],
    '3': [FAQ_3],
    '4': [FAQ_4],
    '5': [FAQ_5],
    '6': [FAQ_6],
    '7': [FAQ_7],
    '8': [FAQ_8],
    'Начать': [HELLO_MESSAGE, mk],
    'Меню': [MENU, st],
    'К.А.В.О.': [FAQ, fq],
    'Вопросы по киту': [KITLIST_MESSAGE, kitlist_q],
    'Защита головы': [HELMET, ck],
    'Защита глаз': [EYE_PROTECTION, ck],
    'Балаклава': [BALACLAVA, ck],
    'Боевая рубашка': [COMBAT_SHIRT, ck],
    'Бронежилет': [PLATE_CARRIER, ck],
    '5-ый, 7-ой слой': [LEVELS, ck],
    'Перчатки': [GLOVES, ck],
    'Штаны': [PANTS, ck],
    'Ботинки': [SHOES, ck],
    'Радиосвязь': [RADIO, ck],
    'Показать категории': [KITLIST_MESSAGE, kitlist_q],
    'Орг. вопросы': [ORG_MESSAGE, org_q],
    'Игры и трены': [CALENDAR],
    'Добор без авто': [TRANSPORT],
    'Как отдыхаем': [RELAX],
    'Помощь новичкам': [NOVICE_HELP],
    'Медиа - ресурсы': [MEDIA_MESSAGE, media_q],
    'О нашей команде': [TEAM_MESSAGE, team_q],
    'Численность': [COUNT],
    'Средний возраст': [MID_AGE],
    'У кого играем': [GAMES],
    'Посещение игр': [GAMES_COUNT],
    'Бонусы команды': [BONUS_MESSAGE, bonus_q],
    'Наши скидки': [DISCOUNTS, DISCOUNTS_NOT_IN_TEAM],
    'Редкие ништяки': [OTHER_COUNTRY, OTHER_COUNTRY_NOT_IN_TEAM],
    'Другие вопросы': [OTHER_MESSAGE, other_q],
    'Ремонт приводов': [MASTER],
    'photo': [WRONG_REQUEST_PHOTO, start],
    'video': [WRONG_REQUEST_VIDEO, start],
    'audio': [WRONG_REQUEST_AUDIO, start],
    'doc': [WRONG_REQUEST_DOC, start],
    'audio_message': [WRONG_REQUEST_AUDIO_MSG, start],
    'graffiti': [WRONG_REQUEST_GRAFFITI, start],
    'geo': [WRONG_REQUEST_GEO, start],
    'no_category': [WRONG_REQUEST, start],
    'wall': [WRONG_REQUEST_WALL, start],
    'wall_reply': [WRONG_REQUEST_WALL_REPLY, start],
    'link': [WRONG_REQUEST_LINK, start],
    'gift': [WRONG_REQUEST_GIFT, start],
    'market': [WRONG_REQUEST_MARKET, start],
    'market_album': [WRONG_REQUEST_MARKET_ALBUM, start],
    'sticker': [WRONG_REQUEST_STICKER, start],
    'text': [WRONG_REQUEST, start]
}
