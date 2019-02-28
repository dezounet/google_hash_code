from collections import defaultdict

from slide import Slide


def search_by_tag(dict_pics):
    """

    :param dict_pics: dict of Pictures with ids as keys
    :return:
    """
    pictures_per_tag = format_input(dict_pics)
    print('total tag count:', len(pictures_per_tag))

    # Filter tag with only one pic
    pictures_per_tag = {k: v for k, v in pictures_per_tag.items() if len(v) > 1}
    print('useful tag count:', len(pictures_per_tag))

    # get first pic

    remaining_picture_ids = set(dict_pics.keys())
    first_picture_id = list(pictures_per_tag.values())[0][0]
    first_picture = dict_pics[first_picture_id]
    remove_pictures_from_dict(first_picture, pictures_per_tag)
    remaining_picture_ids.remove(first_picture_id)
    slideshow = [Slide(first_picture)]

    is_remaining_picture = True
    while is_remaining_picture:
        next_picture_id = get_next_picture(first_picture, pictures_per_tag)
        if next_picture_id:
            remove_pictures_from_dict(dict_pics[next_picture_id], pictures_per_tag)
            slideshow.append(Slide(dict_pics[next_picture_id]))

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
        pictures_per_tag[tag].remove(picture.id)


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


def get_picture_ids_w_tag(list_pictures, tag):
    """

    :param list_pictures:
    :param tag:
    :return:
    """
    return [p.id for p in list_pictures if tag in p.tags]


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
            return pictures_per_tag[tag].pop()
        except IndexError:
            pass

    return None
