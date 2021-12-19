import sys
import re

from fastapi import FastAPI, Request, Depends, HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response, RedirectResponse

from sqlalchemy.orm import Session

from vk.exceptions import VkAPIError

from buttons import button, show_more
from vkapi import is_member, keyboard_button, check_type, instant_message_delete, send_message, send_search_result
from settings.settings import CONFIRMATION_TOKEN, OPEN_GROUP_TOKEN, CLOSED_GROUP_TOKEN, ADMINISTRATORS, TEAM_ONLY_ANSWERS, \
    AUTH_TOKEN

from vkbot_sql import crud, models, schemas
from vkbot_sql.database import engine
from get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

users_of_search = {}


@app.post('/')
async def processing(vk: Request):
    data = await vk.json()

    if 'type' not in data.keys():
        return Response(content='not vk')
    if data['type'] == 'confirmation':
        return Response(content=CONFIRMATION_TOKEN)
    elif data['type'] == 'message_new':

        text = data['object']['message']['text']  # get text from message
        user_id = data['object']['message']['from_id']  # get user ID from message
        peer_id = data['object']['message']['peer_id']  # get peer ID from message
        membership = await is_member(CLOSED_GROUP_TOKEN, '159016402', user_id)
        message = text.split(' ', 1)[-1]
        message = re.sub(r'[^A-ZА-Яa-zа-я0-9\.&\s-]+', ' ', message)
        message = '&'.join(message.split())

        # working with chat bot out of chats
        if user_id == peer_id:

            # function of searching for goods in the database

            if message.lower() != 'поиск' and text.lower().startswith('поиск'):
                if crud.search_db(message, next(get_db())):  # if object exist in database
                    if not users_of_search.get(user_id):  # if user not exist in dictionary

                        users_of_search[user_id] = {}
                        users_of_search[user_id]['result'] = iter(crud.search_db(message, next(get_db())))
                        try:
                            result = next(users_of_search[user_id]['result'])
                            await send_search_result(OPEN_GROUP_TOKEN, user_id,
                                                     f"Сдержание объявления:\n\n{result[0][:4000]}\n\n"
                                                     f"Ссылка: {result[1]}", keyboard=show_more)
                        except Exception as err:
                            print(f'Ошибка в блоке user not exist: {err}')
                            await send_message(OPEN_GROUP_TOKEN, user_id, 'Что-то пошло не так или ничего не найдено, '
                                                                          'попробуйте поискать еще раз.')
                    else:  # if user exist in dictionary
                        users_of_search[user_id]['result'] = iter(crud.search_db(message, next(get_db())))
                        try:
                            result = next(users_of_search[user_id]['result'])
                            await send_search_result(OPEN_GROUP_TOKEN, user_id,
                                                     f"Сдержание объявления:\n\n{result[0][:4000]}\n\n"
                                                     f"Ссылка: {result[1]}", keyboard=show_more)
                        except Exception as err:
                            print(f'Ошибка в блоке user exist: {err}')
                            await send_message(OPEN_GROUP_TOKEN, user_id, 'Что-то пошло не так или ничего не найдено, '
                                                                          'попробуйте поискать еще раз.')
                else:  # if object not exist in database
                    await send_message(OPEN_GROUP_TOKEN, user_id, 'Ничего не найдено, '
                                                                  'попробуйте другой поисковой запрос.')

            # simple check, what user do: sending text, sending attachments or pushing the buttons
            elif 'payload' in data['object']['message']:
                if text == 'Показать еще':  # check for payload button while searching
                    try:
                        result = next(users_of_search[user_id]['result'])
                        await send_search_result(OPEN_GROUP_TOKEN, user_id,
                                                 f"Сдержание объявления:\n\n{result[0][:4000]}\n\n"
                                                 f"Ссылка: {result[1]}", keyboard=show_more)
                    except Exception as err:
                        print(f'Все просмотрено, поэтому выдана ошибка: {err}')
                        await send_message(OPEN_GROUP_TOKEN, user_id, 'Больше результатов нет, начните поиск заново.')
                else:
                    # below is the main functionality of the bot
                    try:
                        if text.lower() in TEAM_ONLY_ANSWERS and membership:
                            if text.lower() in TEAM_ONLY_ANSWERS[1].lower():
                                await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button[text][0],
                                                      attachment='doc-159016402_583562872')
                            else:
                                await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button[text][0])
                        elif text.lower() in TEAM_ONLY_ANSWERS and not membership:
                            await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button[text][1])
                        else:
                            await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text,
                                                  button[text][0], button[text][1])
                    except IndexError:
                        await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button[text][0])

            # if user send to bot his geolocation, bot will understand that and answer to user with the joke
            elif 'geo' in data['object']['message'].keys():
                await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button['geo'][0], button['geo'][1])

            # another one check for attachments with funny results for user
            else:
                if data['object']['message']['attachments']:
                    unpacked_dict = next(iter(data['object']['message']['attachments'][0].values()))
                    await check_type(text, data)
                    await keyboard_button(
                        OPEN_GROUP_TOKEN, user_id, data, text, button[unpacked_dict][0], button[unpacked_dict][1])
                else:
                    await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button['text'][0], button['text'][1])

        # delete all messages from not allowed users in specific chat
        else:
            conversation_message_id = data['object']['message']['conversation_message_id']

            # deleting all messages not from administrators
            try:
                if user_id not in ADMINISTRATORS:
                    await instant_message_delete(OPEN_GROUP_TOKEN, peer_id, conversation_message_id)
            except VkAPIError as err_msg:
                print(err_msg, file=sys.stderr)

    return Response(content='ok')


@app.get('/', response_class=RedirectResponse, status_code=302)
def fake_main():
    return 'https://youtu.be/Q-DXtTDYfg8'


@app.post('/add_items/')
def add_item(request: Request, item: schemas.ItemBase, db: Session = Depends(get_db)):
    auth = request.headers.get('auth')
    if not auth or auth != AUTH_TOKEN:
        return HTTPException(status_code=401, detail='Access denied')
    db_item = crud.get_item_by_link(db, link=item.link)
    if db_item:
        raise HTTPException(status_code=400, detail='Item link already exists')
    return crud.create_item(db=db, item=item)


@app.get('/add_items/', response_class=RedirectResponse, status_code=302)
def add_item():
    return 'https://youtu.be/g4x-l5-iVN8'
