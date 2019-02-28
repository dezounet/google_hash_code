class Slide(object):

    def __init__(self, pic_a, pic_b=None):
        self.pic_a = pic_a
        self.pic_b = pic_b
        self.tags = pic_a.tags

        if self.pic_b is not None:
            self.tags.update(self.pic_b.tags)

    def is_valid(self, pic_b=None):
        if pic_b is None:
            pic_b = self.pic_b

        return (self.pic_a.orientation == 0 and pic_b is None) or \
               (self.pic_a.orientation == 1 and pic_b.orientation == 1)

    def can_add(self, pic_b):
        output = False

        if self.pic_b is None and self.is_valid(pic_b):
            output = True

        return output
