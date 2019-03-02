class Slide(object):

    def __init__(self, pic_a, pic_b=None):
        self.pic_a = pic_a
        self.pic_b = pic_b
        self.tags = pic_a.tags
        self.orientation = pic_a.orientation

        if self.pic_b is not None:
            self.tags.update(self.pic_b.tags)

    def is_valid(self, pic_b=None):
        if pic_b is None:
            pic_b = self.pic_b

        return (self.pic_a.orientation == 0 and pic_b is None) or \
               (self.pic_a.orientation == 1 and pic_b.orientation == 1)

    def add(self, pic_b):
        assert self.pic_a.orientation == 1
        assert pic_b.orientation == 1

        self.pic_b = pic_b
        self.tags = self.tags.union(pic_b.tags)
