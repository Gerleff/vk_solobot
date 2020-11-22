"""
:authors: gerleffx2
:license:
:copyright: (c) 2019 gerleffx2
"""
import sys
import traceback
import vk_api
import logging
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests
import vk_parser
from buttons import korm, photo_give, wall_give
import OpenSSL
from config import group_token, group_id, app_id, owner_id, bye_message, \
    err_log_path, fixer_id, kb_message


def keyboard_in(vk, event):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Получить картинку', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label='Получить пост', color=VkKeyboardColor.PRIMARY)
    # keyboard.add_line()
    # keyboard.add_button(label='Покормить админа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_vkapps_button(app_id=app_id,  # Приложение(для рассылки)
                               owner_id=owner_id,
                               label="Заказать рекламу",
                               hash="sendKeyboard")

    keyboard = keyboard.get_keyboard()
    try:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            random_id=get_random_id(),
            keyboard=keyboard,
            message=' ')
    except KeyError:
        vk.messages.send(
            peer_id=event.obj['from_id'],
            random_id=get_random_id(),
            keyboard=keyboard,
            message=' ')

    except vk_api.exceptions.ApiError:
        try:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                random_id=get_random_id(),
                keyboard=keyboard,
                message=kb_message)
        except KeyError:
            vk.messages.send(
                peer_id=event.obj['from_id'],
                random_id=get_random_id(),
                keyboard=keyboard,
                message=kb_message)


def main():
    vk_session = vk_api.VkApi(token=group_token)
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    def answers(text):
        if text.capitalize() == 'Начать':
            keyboard_in(vk, event)
        elif text == 'Получить картинку':
            photo_give(vk, event)
        elif text == 'Получить пост':
            wall_give(vk, event)
        elif text == 'Покормить админа':
            korm(vk, event)
        else:
            keyboard_in(vk, event)

    for event in longpoll.listen():
        logging.info(event)
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.obj.message['text'])
            try:
                answers(event.obj.message['text'])
            except vk_api.exceptions.ApiError:
                raise

            except:
                raise
        elif event.type == VkBotEventType.GROUP_LEAVE:

            try:
                vk.messages.send(
                    user_id=event.obj['user_id'],
                    random_id=get_random_id(),
                    message=bye_message
                )
            except:
                pass


if __name__ == '__main__':

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    while True:
        try:
            main()
        except requests.exceptions.ReadTimeout:
            continue
        except OpenSSL.SSL.WantReadError:
            continue
        except:
            exc_info = sys.exc_info()
            formated_error = traceback.format_exception(*exc_info)
            logging.info(formated_error)
            continue
