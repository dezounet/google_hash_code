from collections import defaultdict

from slide import Slide

from random import randint


def search_by_tag(dict_pics, pictures_per_tag):
    """

    :param dict_pics: dict of Pictures with ids as keys
    :return:
    """

    available_tag = set(pictures_per_tag.keys())
    for i, pic in dict_pics.items():
        pic.tags = pic.tags & available_tag

    # get first pic
    pic = None
    size = len(dict_pics)
    while pic is None:
        pic = dict_pics.get(randint(0, size))

    pictures_per_tag = remove_pictures_from_dict(pic, pictures_per_tag)

    # initialize slides
    slideshow = [Slide(pic)]

    is_remaining_picture = True
    while is_remaining_picture:
        next_pic_id = get_next_picture(pic, pictures_per_tag, dict_pics)

        if next_pic_id is not None:
            next_pic = dict_pics[next_pic_id]
            pictures_per_tag = remove_pictures_from_dict(next_pic, pictures_per_tag)

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
            if len(pictures_per_tag[tag]) == 0:
                del pictures_per_tag[tag]

        except KeyError:
            pass

    return pictures_per_tag


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

    pictures_per_tags = dict(pictures_per_tags)
    return pictures_per_tags


def get_next_picture(picture, pictures_per_tag, remaining_id):
    """

    :param picture:
    :param pictures_per_tag:
    :return:
    """

    potential_next_picture_tags = picture.tags & set(pictures_per_tag)
    if len(potential_next_picture_tags) == 0:
        print('stooooop!')
        return None

    eligible_ids = []
    for tag in potential_next_picture_tags:
        eligible_ids += list(pictures_per_tag[tag])

    next_id = None
    current_len = 0

    eligible_ids = set(eligible_ids)
    for id in eligible_ids:
        if current_len < len(remaining_id[id].tags):
            current_len = len(remaining_id[id].tags)
            next_id = id

    if next_id is not None:
        print('continuing!')
        return next_id
    else:
        print('stooooop!')
        return None
