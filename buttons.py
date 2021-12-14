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
    '1': [get_answer('FAQ_1')],
    '2': [get_answer('FAQ_2')],
    '3': [get_answer('FAQ_3')],
    '4': [get_answer('FAQ_4')],
    '5': [get_answer('FAQ_5')],
    '6': [get_answer('FAQ_6')],
    '7': [get_answer('FAQ_7')],
    '8': [get_answer('FAQ_8')],
    'Начать': [get_answer('HELLO_MESSAGE'), main],
    'Меню': [get_answer('MENU'), menu],
    'К.А.В.О.': [get_answer('FAQ'), faq],
    'Вопросы по киту': [get_answer('KITLIST_MESSAGE'), loadout],
    'Защита головы': [get_answer('HELMET'), categories],
    'Защита глаз': [get_answer('EYE_PROTECTION'), categories],
    'Балаклава': [get_answer('BALACLAVA'), categories],
    'Боевая рубашка': [get_answer('COMBAT_SHIRT'), categories],
    'Бронежилет': [get_answer('PLATE_CARRIER'), categories],
    '5-ый, 7-ой слой': [get_answer('LEVELS'), categories],
    'Перчатки': [get_answer('GLOVES'), categories],
    'Штаны': [get_answer('PANTS'), categories],
    'Ботинки': [get_answer('SHOES'), categories],
    'Радиосвязь': [get_answer('RADIO'), categories],
    'Показать категории': [get_answer('KITLIST_MESSAGE'), loadout],
    'Орг. вопросы': [get_answer('ORG_MESSAGE'), org],
    'Игры и трены': [get_answer('CALENDAR')],
    'Добор без авто': [get_answer('TRANSPORT')],
    'Как отдыхаем': [get_answer('RELAX')],
    'Помощь новичкам': [get_answer('NOVICE_HELP')],
    'Медиа - ресурсы': [get_answer('MEDIA_MESSAGE'), media],
    'О нашей команде': [get_answer('TEAM_MESSAGE'), team],
    'Численность': [get_answer('COUNT')],
    'Средний возраст': [get_answer('MID_AGE')],
    'У кого играем': [get_answer('GAMES')],
    'Посещение игр': [get_answer('GAMES_COUNT')],
    'Бонусы команды': [get_answer('BONUS_MESSAGE'), bonus],
    'Наши скидки': [get_answer('DISCOUNTS'), DISCOUNTS_NOT_IN_TEAM],
    'Редкие ништяки': [get_answer('OTHER_COUNTRY'), OTHER_COUNTRY_NOT_IN_TEAM],
    'Другие вопросы': [get_answer('OTHER_MESSAGE'), other],
    'Ремонт приводов': [get_answer('MASTER')],
    'photo': [get_answer('WRONG_REQUEST_PHOTO'), start],
    'video': [get_answer('WRONG_REQUEST_VIDEO'), start],
    'audio': [get_answer('WRONG_REQUEST_AUDIO'), start],
    'doc': [get_answer('WRONG_REQUEST_DOC'), start],
    'audio_message': [get_answer('WRONG_REQUEST_AUDIO_MSG'), start],
    'graffiti': [get_answer('WRONG_REQUEST_GRAFFITI'), start],
    'geo': [get_answer('WRONG_REQUEST_GEO'), start],
    'no_category': [get_answer('WRONG_REQUEST'), start],
    'wall': [get_answer('WRONG_REQUEST_WALL'), start],
    'wall_reply': [get_answer('WRONG_REQUEST_WALL_REPLY'), start],
    'link': [get_answer('WRONG_REQUEST_LINK'), start],
    'gift': [get_answer('WRONG_REQUEST_GIFT'), start],
    'market': [get_answer('WRONG_REQUEST_MARKET'), start],
    'market_album': [get_answer('WRONG_REQUEST_MARKET_ALBUM'), start],
    'sticker': [get_answer('WRONG_REQUEST_STICKER'), start],
    'text': [get_answer('WRONG_REQUEST'), start]
}
