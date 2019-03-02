import random
import copy

from slide import Slide
from score import transition_score


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
                    if transition_score(current_slide, previous_slide):
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(current_slide)
                        previous_slide = current_slide

        return slideshow

    def greedy_random_horizontal_make(self, pics):
        slideshow = []

        previous_slide = None

        index = list(range(len(pics)))
        random.shuffle(index)

        for i in index:
            pic = pics[i]

            # First, only Horizontal
            if pic.orientation == 1:
                continue

            current_slide = Slide(pic, None)

            if current_slide.is_valid():  # Horizontal
                if previous_slide is None:
                    slideshow.append(current_slide)
                    previous_slide = current_slide
                else:
                    if transition_score(current_slide, previous_slide):
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(current_slide)
                        previous_slide = current_slide

        return slideshow

    def greedy_vertical_make(self, pics):
        slideshow = []

        previous_slide = None
        current_slide = None

        pics_copy = copy.copy(pics)
        keep_going = True

        while keep_going:
            current_slideshow = []

            for i, pic in pics_copy.items():
                # First, only Vertical
                if pic.orientation == 0:
                    continue

                if current_slide is None:
                    current_slide = Slide(pic, None)
                    continue
                else:
                    current_slide.add(pic)

                if current_slide.is_valid():
                    if previous_slide is None:
                        slideshow.append(current_slide)
                        current_slideshow.append(current_slide)

                        previous_slide = current_slide
                    else:
                        if transition_score(current_slide, previous_slide):
                            # Ok, current slide is valid, add it to slideshow
                            slideshow.append(current_slide)
                            current_slideshow.append(current_slide)

                            previous_slide = current_slide

                    current_slide = None

            if not current_slideshow:
                # Stop when no more slideshow found
                keep_going = False
            else:
                # print('Adding %s slides' % len(current_slideshow))
                for slide in current_slideshow:
                    del pics_copy[slide.pic_a.id]
                    del pics_copy[slide.pic_b.id]

        return slideshow

    def greedy_random_vertical_make(self, pics):
        slideshow = []

        previous_slide = None
        current_slide = None

        pics_copy = copy.copy(pics)
        keep_going = True

        # print('Starting greedy slideshow maker...')
        while keep_going:
            current_slideshow = []

            index = list(pics_copy.keys())
            random.shuffle(index)

            for i in index:
                pic = pics_copy[i]

                # First, only Vertical
                if pic.orientation == 0:
                    continue

                if current_slide is None:
                    current_slide = Slide(pic, None)
                    continue
                else:
                    current_slide.add(pic)

                if current_slide.is_valid():
                    if previous_slide is None:
                        slideshow.append(current_slide)
                        current_slideshow.append(current_slide)

                        previous_slide = current_slide
                    else:
                        if transition_score(current_slide, previous_slide):
                            # Ok, current slide is valid, add it to slideshow
                            slideshow.append(current_slide)
                            current_slideshow.append(current_slide)

                            previous_slide = current_slide

                    current_slide = None

            if not current_slideshow:
                # Stop when no more slideshow found
                keep_going = False
            else:
                # print('Adding %s slides' % len(current_slideshow))
                for slide in current_slideshow:
                    del pics_copy[slide.pic_a.id]
                    del pics_copy[slide.pic_b.id]

        return slideshow

    def greedy_random_make(self, slides):
        slideshow = []

        previous_slide = None

        slides = copy.copy(slides)

        keep_going = True
        while keep_going:
            current_slideshow = []

            index = list(list(slides.keys()))
            random.shuffle(index)

            for i in index:
                slide = slides[i]

                if previous_slide is None:
                    slideshow.append(slide)
                    current_slideshow.append(i)

                    previous_slide = slide
                else:
                    if transition_score(slide, previous_slide):
                        # Ok, current slide is valid, add it to slideshow
                        slideshow.append(slide)
                        current_slideshow.append(i)

                        previous_slide = slide

            if not current_slideshow:
                # Stop when no more slideshow found
                keep_going = False
            else:
                # print('Adding %s slides' % len(current_slideshow))
                for slide_id in current_slideshow:
                    del slides[slide_id]

        return slideshow

    def greedy_best_make(self, slides):
        slideshow = []

        slides = copy.copy(slides)

        # Randomly pick first pick
        index = list(slides.keys())
        starting_index = random.choice(index)
        previous_slide = slides.pop(starting_index)
        slideshow.append(previous_slide)

        keep_going = True
        while keep_going:
            current_slide_id = self._find_best_transition(slides, previous_slide)

            if current_slide_id is None:
                # Stop when no more slideshow found
                keep_going = False
            else:
                slideshow.append(slides[current_slide_id])

                previous_slide = slides[current_slide_id]
                del slides[current_slide_id]

        return slideshow

    def _find_best_transition(self, slides, previous_slide):
        best_transition = 0
        best_slide_id = None

        for i, current_slide in slides.items():
            current_transition = transition_score(previous_slide, current_slide)

            if current_transition > best_transition:
                best_transition = current_transition
                best_slide_id = i

        return best_slide_id
