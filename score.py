def transition_score(slide1, slide2):
    """
    Compute score between two Slides
    :param slide1: Slide
    :param slide2: Slide
    :return:
    """
    tags_slide1 = slide1.tags
    tags_slide2 = slide2.tags
    common_tags = tags_slide1 & tags_slide2

    tags_only_slide1 = tags_slide1 - common_tags
    tags_only_slide2 = tags_slide2 - common_tags

    return min(len(tags_only_slide1), len(tags_only_slide2), len(common_tags))


def slideshow_score(list_slides):
    """
    Compute score of a slideshow represented as a list of slides
    :param list_slides:
    :return:
    """
    score = sum([transition_score(list_slides[i], list_slides[i+1]) for i in range(len(list_slides) - 1)])

    return score
