from collections import defaultdict

from slide import Slide

import random
from random import randint


def search_by_tag(dict_pics):
    """

    :param dict_pics: dict of Pictures with ids as keys
    :return:
    """
    # horizontal
    dict_pics = {k: v for k, v in dict_pics.items() if v.orientation == 0}

    pictures_per_tag = format_input(dict_pics)
    # print('total tag count:', len(pictures_per_tag))

    # Filter tag with only one pic
    pictures_per_tag = {k: v for k, v in pictures_per_tag.items() if len(v) > 1}
    # print('useful tag count:', len(pictures_per_tag))

    # get first pic
    pic = None
    size = len(dict_pics)
    while pic is None:
        pic = dict_pics.get(randint(0, size))

    remove_pictures_from_dict(pic, pictures_per_tag)

    # initialize slides
    slideshow = [Slide(pic)]

    is_remaining_picture = True
    while is_remaining_picture:
        next_pic_id = get_next_picture(pic, pictures_per_tag)

        if next_pic_id:
            next_pic = dict_pics[next_pic_id]
            remove_pictures_from_dict(next_pic, pictures_per_tag)

            slideshow.append(Slide(next_pic))

        else:
            is_remaining_picture = False

    return slideshow


def remove_pictures_from_dict(picture, pictures_per_tag):
    """

    :param picture: Phpoto
    :param pictures_per_tag:
    :return:
    """
    for tag in picture.tags:
        try:
            pictures_per_tag[tag].remove(picture.id)

            # remove empty keys
            if not pictures_per_tag[tag]:
                del pictures_per_tag[tag]
        except KeyError:
            pass


def format_input(dict_pics):
    """
    Format the dict of pics to a dict with tags as keys and set of Picture as values
    :param dict_pics:
    :return:
    """
    pictures = dict_pics.values()

    pictures_per_tags = defaultdict(set)

    for pic in pictures:
        for tag in pic.tags:
            pictures_per_tags[tag].add(pic.id)

    return pictures_per_tags


def get_next_picture(picture, pictures_per_tag):
    """

    :param picture:
    :param pictures_per_tag:
    :return:
    """
    potential_next_picture_tags = picture.tags & set(pictures_per_tag)
    if len(potential_next_picture_tags) == 0:
        return None

    for tag in potential_next_picture_tags:
        try:
            choice = random.choice(tuple(pictures_per_tag[tag]))
            pictures_per_tag[tag].remove(choice)
            return choice
        except KeyError:
            pass

    return None
