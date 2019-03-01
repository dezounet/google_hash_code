import sys
import os

from collections import Counter
from collections import defaultdict


def get_pics_per_tags(pics):
    """
    Format the dict of pics to a dict with tags as keys and set of Picture as values
    """
    pictures = pics.values()
    pictures_per_tags = defaultdict(set)

    for pic in pictures:
        for tag in pic.tags:
            pictures_per_tags[tag].add(pic.id)

    # From default dict to dict
    pictures_per_tags = dict(pictures_per_tags)

    return pictures_per_tags


if __name__ == '__main__':

    from config import INPUT_DIRECTORY
    from config import COUNTER_DIRECTORY

    from InputReader import InputReader


    def write_counter(counter, filename):
        with open(filename, 'w') as f:
            f.write('%s %s\n' % (len(counter), sum(counter.values())))
            for tag, count in counter.most_common():
                f.write('%s %s\n' % (tag, count))


    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    # Get objects from input file
    inputReader = InputReader(file_path)

    counter = Counter()
    for i, pic in inputReader.photos.items():
        current_counter = Counter(pic.tags)
        counter.update(current_counter)

    # Save result to output file
    output_file = os.path.splitext(input_file)[0] + '.count'
    out_path = os.path.join(COUNTER_DIRECTORY, output_file)

    write_counter(counter, out_path)
