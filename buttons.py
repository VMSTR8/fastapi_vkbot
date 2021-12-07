import json

from vkbot_sql.crud import get_answer

from answers import *

with open('./keyboards/start_bot.json', 'r', encoding='utf-8') as start_bot_keyboard, \
        open('./keyboards/main_keyboard.json', 'r', encoding='utf-8') as main_keyboard, \
        open('./keyboards/start_menu.json', 'r', encoding='utf-8') as start_menu_keyboard, \
        open('./keyboards/faq_keyboard.json', 'r', encoding='utf-8') as faq_keyboard_keyboard, \
        open('./keyboards/categories_keyboard.json', 'r', encoding='utf-8') as categories_keyboard, \
        open('./keyboards/kitlist.json', 'r', encoding='utf-8') as kitlist_keyboard, \
        open('./keyboards/orq_questions.json', 'r', encoding='utf-8') as orq_questions_keyboard, \
        open('./keyboards/media_keyboard.json', 'r', encoding='utf-8') as media_keyboard, \
        open('./keyboards/about_team_keyboard.json', 'r', encoding='utf-8') as about_team_keyboard, \
        open('./keyboards/bonus_keyboard.json', 'r', encoding='utf-8') as bonus_keyboard, \
        open('./keyboards/other_questions_keyboard.json', 'r', encoding='utf-8') as other_questions_keyboard, \
        open('./keyboards/show_more.json', 'r', encoding='utf-8') as show_more_keyboard:

    start = json.dumps(json.load(start_bot_keyboard))
    main = json.dumps(json.load(main_keyboard))
    menu = json.dumps(json.load(start_menu_keyboard))
    faq = json.dumps(json.load(faq_keyboard_keyboard))
    categories = json.dumps(json.load(categories_keyboard))
    loadout = json.dumps(json.load(kitlist_keyboard))
    org = json.dumps(json.load(orq_questions_keyboard))
    media = json.dumps(json.load(media_keyboard))
    team = json.dumps(json.load(about_team_keyboard))
    bonus = json.dumps(json.load(bonus_keyboard))
    other = json.dumps(json.load(other_questions_keyboard))
    show_more = json.dumps(json.load(show_more_keyboard))

button = {
    '1': [FAQ_1],
    '2': [FAQ_2],
    '3': [FAQ_3],
    '4': [FAQ_4],
    '5': [FAQ_5],
    '6': [FAQ_6],
    '7': [FAQ_7],
    '8': [FAQ_8],
    'Начать': [HELLO_MESSAGE, main],
    'Меню': [MENU, menu],
    'К.А.В.О.': [FAQ, faq],
    'Вопросы по киту': [KITLIST_MESSAGE, loadout],
    'Защита головы': [HELMET, categories],
    'Защита глаз': [EYE_PROTECTION, categories],
    'Балаклава': [BALACLAVA, categories],
    'Боевая рубашка': [COMBAT_SHIRT, categories],
    'Бронежилет': [PLATE_CARRIER, categories],
    '5-ый, 7-ой слой': [LEVELS, categories],
    'Перчатки': [GLOVES, categories],
    'Штаны': [PANTS, categories],
    'Ботинки': [SHOES, categories],
    'Радиосвязь': [RADIO, categories],
    'Показать категории': [KITLIST_MESSAGE, loadout],
    'Орг. вопросы': [ORG_MESSAGE, org],
    'Игры и трены': [CALENDAR],
    'Добор без авто': [TRANSPORT],
    'Как отдыхаем': [RELAX],
    'Помощь новичкам': [NOVICE_HELP],
    'Медиа - ресурсы': [MEDIA_MESSAGE, media],
    'О нашей команде': [TEAM_MESSAGE, team],
    'Численность': [COUNT],
    'Средний возраст': [MID_AGE],
    'У кого играем': [GAMES],
    'Посещение игр': [GAMES_COUNT],
    'Бонусы команды': [BONUS_MESSAGE, bonus],
    'Наши скидки': [DISCOUNTS, DISCOUNTS_NOT_IN_TEAM],
    'Редкие ништяки': [OTHER_COUNTRY, OTHER_COUNTRY_NOT_IN_TEAM],
    'Другие вопросы': [OTHER_MESSAGE, other],
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
