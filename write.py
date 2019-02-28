import output_slides


class OutputWriter:
    def __init__(self, filename, outputSlidesCol):
        self.filename = filename
        self.outputSlidesCol = outputSlidesCol

    def write(self):
        with open(self.filename, 'w') as f:
            f.write(len(self.outputSlidesCol))
            f.write("\n")
            for slide in self.outputSlidesCol:
                f.write('%(num)' % slide[0])
                if slide[1] is not None:
                    f.write(' %(num)', slide[1])
                f.write("\n")