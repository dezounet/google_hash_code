import sys
import os

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

# from read import read
from write import write
from InputReader import InputReader

from slideshow_maker import SlideshowMaker

if __name__ == '__main__':
    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    # Get objects from input file
    inputReader = InputReader(file_path)

    output = None
    output_horizontal = slideshow_maker.greedy_horizontal_make(inputReader.photos)
    output_horizontal_reverse = slideshow_maker.greedy_reverse_horizontal_make(inputReader.photos)
    output_vertical = slideshow_maker.greedy_vertical_make(inputReader.photos)

    if len(output_horizontal_reverse) > len(output_horizontal):
        output_horizontal = output_horizontal_reverse
    from search_by_tag import search_by_tag
    output = search_by_tag(inputReader.photos)

    output = output_horizontal + output_vertical
    print('found solution with', len(output), 'slides')

    # Save result to output file
    output_file = os.path.splitext(input_file)[0] + '.out'
    out_path = os.path.join(OUTPUT_DIRECTORY, output_file)

    write(output, out_path)
