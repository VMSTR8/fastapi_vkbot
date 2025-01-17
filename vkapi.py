import random

import vk

session = vk.Session()
api = vk.API(session, v='5.131')


async def check_type(text, json):
    if [i for i in json['object']['message']['attachments'] if text in i]:
        return True


async def send_message(access_token, user_id, message, attachment='', keyboard=''):
    api.messages.send(access_token=access_token,
                      user_id=str(user_id),
                      message=message,
                      attachment=attachment,
                      keyboard=keyboard,
                      random_id=random.getrandbits(64),
                      dont_parse_links=1)


async def send_search_result(access_token, user_id, message, attachment='', keyboard=''):
    api.messages.send(access_token=access_token,
                      user_id=str(user_id),
                      message=message,
                      attachment=attachment,
                      keyboard=keyboard,
                      random_id=random.getrandbits(64),
                      dont_parse_links=0)


async def keyboard_button(access_token, user_id, json, request, message, keyboard='', attachment=''):
    if str(request) in json['object']['message']['text']:
        api.messages.send(access_token=access_token,
                          user_id=str(user_id),
                          message=message,
                          keyboard=keyboard,
                          attachment=attachment,
                          random_id=random.getrandbits(64),
                          dont_parse_links=1)


async def instant_message_delete(access_token, peer_id, conversation_message_ids=list):
    api.messages.delete(access_token=access_token,
                        peer_id=peer_id,
                        conversation_message_ids=conversation_message_ids,
                        delete_for_all=1)


async def is_member(access_token, group_id, user_id):
    return api.groups.isMember(access_token=access_token,
                               group_id=group_id,
                               user_id=user_id)


# функция не используется, оставлена на всякий случай
# def search_handler(message, offset):
#     job = search_db(query=message, db=next(get_db()))[offset:offset + 1]
#     return '\n'.join([f'{i[0][:4000]}\n\nСсылка: {i[1]}\n{"=" * 15}\n' for i in job])
