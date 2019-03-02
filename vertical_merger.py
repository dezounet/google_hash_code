import random
from copy import copy

from slide import Slide


def merge(vertical_pics):
    slides = []

    # Do not update input struct
    vertical_pics_copy = copy(vertical_pics)

    unmatched_pics = {}

    # for every pic, found a non overlapping pic
    print('find perfect vertical matching (%s)...' % len(vertical_pics_copy))
    keep_going = True
    while keep_going:
        if len(vertical_pics_copy) < 2:
            keep_going = False
        else:
            first_pic = vertical_pics_copy.pop(random.choice(list(vertical_pics_copy.keys())))
            second_pic = None

            for i, pic in vertical_pics_copy.items():
                if not set(first_pic.tags) & set(pic.tags):
                    second_pic = pic
                    break

            if second_pic is not None:
                del vertical_pics_copy[second_pic.id]
                slides.append(Slide(first_pic, second_pic))
            else:
                unmatched_pics[first_pic.id] = first_pic

    # for the remaining pics, match it with the less overlapping
    print('find remaining vertical matching (%s)...' % len(unmatched_pics))
    keep_going = True
    while keep_going:
        if len(unmatched_pics) < 2:
            keep_going = False
        else:
            first_pic = unmatched_pics.pop(random.choice(list(unmatched_pics.keys())))
            second_pic = None

            tag_count = 0
            for i, pic in unmatched_pics.items():
                current_tag_count = len(set(first_pic.tags) | set(pic.tags))
                if current_tag_count > tag_count:
                    second_pic = pic
                    tag_count = current_tag_count

            del unmatched_pics[second_pic.id]

            slides.append(Slide(first_pic, second_pic))

    return slides
