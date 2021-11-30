import sys

from fastapi import FastAPI, Request, Depends, HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from sqlalchemy.orm import Session

from vk.exceptions import VkAPIError

from buttons import button
from vkapi import is_member, keyboard_button, check_type, instant_message_delete
from settings import CONFIRMATION_TOKEN, OPEN_GROUP_TOKEN, CLOSED_GROUP_TOKEN, ADMINISTRATORS, TEAM_ONLY_ANSWERS

from vkbot_sql import crud, models, schemas
from vkbot_sql.database import engine
from get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)


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

        # working with chat bot out of chats
        if user_id == peer_id:

            # simple check, what user do: sending text, sending attachments or pushing the buttons
            if 'payload' in data['object']['message']:
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


@app.post('/add_items/', response_model=schemas.ItemBase)
def add_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_link(db, link=item.link)
    if db_item:
        raise HTTPException(status_code=400, detail='Item link already exists')
    return crud.create_item(db=db, item=item)
