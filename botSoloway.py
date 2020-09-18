"""
:authors: gerleffx2
:license:
:copyright: (c) 2019 gerleffx2
"""
import sys
import traceback
import vk_api
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
    keyboard.add_button(label='Получить картинку', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button(label='Получить пост', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='Покормить админа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_vkapps_button(app_id=app_id,  # Приложение(для рассылки)
                               owner_id=owner_id,
                               label="Заказать рекламу",
                               hash="sendKeyboard")

    try:
        vk.messages.send(
            peer_id=event.obj.message['peer_id'],
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message=' ')
    except KeyError:
        vk.messages.send(
            peer_id=event.obj['from_id'],
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message=' ')

    except vk_api.exceptions.ApiError:
        try:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard(),
                message=kb_message)
        except KeyError:
            vk.messages.send(
                peer_id=event.obj['from_id'],
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard(),
                message=kb_message)


def main():
    vk_session = vk_api.VkApi(token=group_token)
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    def errors_send(vk, log):
        vk.messages.send(
                user_id=fixer_id,
                random_id=get_random_id(),
                message='Возникли новые ошибки! Проверь: {}'.format('\n'.join(log))
            )

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
            pass

    for event in longpoll.listen():
        print(event.type)
       #  if str(datetime.datetime.now().time())[0:1] == '02':
            # vk_parser.data_collect()
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.obj.message['text'])
            try:
                answers(event.obj.message['text'])
            except vk_api.exceptions.ApiError:
                print('Апи сука эррор, детали: ')
                print(event)
                continue
            except Exception as e:
                print('ERROR! ' + str(e))
                exc_info = sys.exc_info()
                formated_error = traceback.format_exception(*exc_info)
                with open(err_log_path, 'r', encoding="utf-8") as f:
                    error_log_list: List[str] = f.readlines()
                    f.close()
                with open(err_log_path, 'a', encoding="utf-8") as f:
                    error_text = str(formated_error[-2] + formated_error[-1] + '\n')
                    if error_text not in str(error_log_list):
                        f.write(error_text)
                        errors_send(vk, error_log_list[-4:-1])
                    f.close()
                    continue
        elif event.type == VkBotEventType.GROUP_LEAVE:
            # print(event.obj)
            try:
                vk.messages.send(
                    user_id=event.obj['user_id'],
                    random_id=get_random_id(),
                    message=bye_message
                )
            except:
                pass

if __name__ == '__main__':
    while True:
        try:
            main()
        except requests.exceptions.ReadTimeout:
            with open('err_log.txt', 'a') as f:
                f.write('\n'+str(datetime.datetime.now().time())+'--->ReadTimeOutError')
                f.close()
            continue
        except OpenSSL.SSL.WantReadError:
            with open('err_log.txt', 'a') as f:
                f.write('\n'+str(datetime.datetime.now().time())+'--->WantReadError')
                f.close()
            continue
        except:
            exc_info = sys.exc_info()
            formated_error = traceback.format_exception(*exc_info)
            error_text = str(formated_error + '\n')
            with open(err_log_path, 'a', encoding="utf-8") as f:
                f.write(error_text)
                f.close()
            continue


