from slide import Slide


class OutputSlides:
    def __init__(self):
        self.slidePairSet = set()

    def add_photos(self, slide):
        if slide.pic_b is not None:
            self.slidePairSet.add((slide.pic_a.id, slide.pic_b.id))
        else:
            self.slidePairSet.add((slide.pic_a.id, None))
