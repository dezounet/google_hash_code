from slide import Slide


class SlideshowMaker(object):
    def __init__(self):
        # Maybe this will be useful
        pass

    def greedy_make(self, pics):
        slideshow = None

        current_slide = None

        for i, pic in pics.items():
            if current_slide is None:
                current_slide = Slide(pic, None)

        return slideshow
