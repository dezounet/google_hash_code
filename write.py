def write(output, filename):
    with open(filename, 'w') as f:
        f.write(str(len(output)))
        f.write('\n')

        for slide in output:
            f.write(str(slide.pic_a.id))
            if slide.pic_b is not None:
                f.write(' %s\n' % slide.pic_b.id)
            else:
                f.write('\n')
