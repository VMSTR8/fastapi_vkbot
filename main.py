import sys
from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response, RedirectResponse

from sqlalchemy.orm import Session

from vk.exceptions import VkAPIError

from buttons import button
from vkapi import is_member, keyboard_button, check_type, instant_message_delete, send_message, search_handler
from settings import CONFIRMATION_TOKEN, OPEN_GROUP_TOKEN, CLOSED_GROUP_TOKEN, ADMINISTRATORS, TEAM_ONLY_ANSWERS, \
    AUTH_TOKEN

from vkbot_sql import crud, models, schemas
from vkbot_sql.database import engine
from get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

users_requests = {}


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

        # working with chat bot out of chats
        if user_id == peer_id:

            # bots search
            # DONE если вбить слово поиск, то он начнет искать по слову поиск -- исправить
            # TODO добавить кнопку "показать еще"
            # TODO рефакторинг когда, переписать в функции то, что можно переписать
            # TODO не забывать про ограничения 4096 символов от вк, обработать это как то покраше
            # TODO создать базу пользователей и запросов пользователей

            if message != 'поиск' and text.lower().startswith('поиск'):

                if not users_requests.get(user_id):

                    users_requests[user_id] = {}
                    users_requests[user_id][message] = 0
                    offset = users_requests[user_id][message]

                    try:
                        await send_message(OPEN_GROUP_TOKEN, user_id, search_handler(message=message, offset=offset))
                        users_requests[user_id][message] += 3
                    except VkAPIError as err:
                        print(err)
                        await send_message(OPEN_GROUP_TOKEN, user_id, "Нечего показывать")

                else:
                    try:
                        offset = users_requests[user_id][message]
                    except KeyError as err:
                        print(err)
                        users_requests[user_id][message] = 0
                        offset = users_requests[user_id][message]
                    try:
                        await send_message(OPEN_GROUP_TOKEN, user_id, search_handler(message=message, offset=offset))
                        users_requests[user_id][message] += 3
                    except VkAPIError as err:
                        print(err)
                        await send_message(OPEN_GROUP_TOKEN, user_id, "Больше нечего показывать")
                        users_requests[user_id][message] = 0

            # simple check, what user do: sending text, sending attachments or pushing the buttons
            elif 'payload' in data['object']['message']:
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
                        await keyboard_button(OPEN_GROUP_TOKEN, user_id, data, text, button[text][0], button[text][1])
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


@app.get('/a_nu_davai/')
def search(query: Optional[str] = None, db: Session = Depends(get_db)):
    job = crud.search_db(query, db=db)
    return job
