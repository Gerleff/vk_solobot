"""
:authors: gerleffx2
:license:
:copyright: (c) 2019 gerleffx2
"""

import vk_parser
from vk_api.utils import get_random_id
from config import korm_message, alb_owner_id, photo_min
from random import randint as r
from data import photo_max


def korm(vk, event):
    try:
        vk.messages.send(
            user_id=event.obj.message['peer_id'],
            random_id=get_random_id(),
            message=korm_message)
    except KeyError:
        vk.messages.send(
            peer_id=event.obj['from_id'],
            random_id=get_random_id(),
            message=korm_message)


def photo_give(vk, event):
    # photo = 'photo' + alb_owner_id + '_' + str(vk_parser.photos_get())
    photo = 'photo' + alb_owner_id + '_' + str(r(photo_min, photo_max))
    try:
        vk.messages.send(
            user_id=event.obj.message['peer_id'],
            random_id=get_random_id(), attachment=photo,
            message='  ')
    except KeyError:
        vk.messages.send(
            peer_id=event.obj['from_id'],
            random_id=get_random_id(), attachment=photo,
            message='  ')


def wall_give(vk, event):
    wall = 'wall' + '-112199313' + '_' + str(vk_parser.post_get())
    try:
        vk.messages.send(
            user_id=event.obj.message['peer_id'],
            random_id=get_random_id(), attachment=wall,
            message='  ')
    except KeyError:
        vk.messages.send(
            peer_id=event.obj['from_id'],
            random_id=get_random_id(), attachment=wall,
            message='  ')
