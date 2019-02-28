from slide import Slide


class SlideshowMaker(object):
    def __init__(self):
        # Maybe this will be useful
        pass

    def greedy_horizontal_make(self, pics):
        slideshow = []

        previous_slide = None

        for i, pic in pics.items():
            # First, only Horizontal
            if pic.orientation == 1:
                continue

            current_slide = Slide(pic, None)

            if current_slide.is_valid():  # Horizontal
                if previous_slide is None:
                    slideshow.append(current_slide)
                    previous_slide = current_slide
                else:
                    if current_slide.tags & previous_slide.tags:
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(current_slide)
                        previous_slide = current_slide

        return slideshow

    def greedy_reverse_horizontal_make(self, pics):
        slideshow = []

        previous_slide = None

        for i, pic in sorted(pics.items(), key=lambda x: x[0], reverse=True):
            # First, only Horizontal
            if pic.orientation == 1:
                continue

            current_slide = Slide(pic, None)

            if current_slide.is_valid():  # Horizontal
                if previous_slide is None:
                    slideshow.append(current_slide)
                    previous_slide = current_slide
                else:
                    if current_slide.tags & previous_slide.tags:
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(current_slide)
                        previous_slide = current_slide

        return slideshow

    def greedy_vertical_make(self, pics):
        slideshow = []

        previous_slide = None
        current_slide = None

        for i, pic in pics.items():
            # First, only Vertical
            if pic.orientation == 0:
                continue

            if current_slide is None:
                current_slide = Slide(pic, None)
                continue
            else:
                current_slide.pic_b = pic

            if current_slide.is_valid():
                if previous_slide is None:
                    slideshow.append(current_slide)
                    previous_slide = current_slide
                else:
                    if current_slide.tags & previous_slide.tags:
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(current_slide)
                        previous_slide = current_slide
                current_slide = None

        return slideshow
