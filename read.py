
def read(filename):
    header = None
    lines = []

    with open(filename) as f:
        for line in f:
            if header is None:
                header = line
            else:
                lines.append(line)

    # TODO

    return None
