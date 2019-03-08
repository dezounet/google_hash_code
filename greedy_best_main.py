import sys
import os

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

from InputReader import InputReader
from write import write

from slide import Slide

from vertical_merger import merge
from slideshow_maker import SlideshowMaker

from score import get_current_best_score
from score import slideshow_score

if __name__ == '__main__':
    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    # Get current best scores
    best_scores = get_current_best_score()
    initial_best_score = best_scores.get(input_file, 0)
    best_score = initial_best_score

    # Get objects from input file
    inputReader = InputReader(file_path)
    pics = inputReader.photos

    horizontal_pics = {k: v for k, v in pics.items() if v.orientation == 0}
    horizontal_pics_id = list(horizontal_pics.keys())

    vertical_pics = {k: v for k, v in pics.items() if v.orientation == 1}
    vertical_pics_id = list(vertical_pics.keys())

    print('Trying to sort %s H pics, %s V pics...' % (len(horizontal_pics_id), len(vertical_pics)))

    # # horizontal slide
    # horizontal_slides = {}
    # for i, pic in horizontal_pics.items():
    #     horizontal_slides[i] = Slide(pic)
    #
    # # Match vertical pics together
    # vertical_slides = merge(vertical_pics)
    #
    # slides = {}
    # slides.update(horizontal_slides)
    # slides.update(vertical_slides)

    # Do better
    output = []

    print('Starting computation...')
    keep_going = True
    i = 0
    while keep_going:
        try:
            current_output = SlideshowMaker().greedy_on_pics(pics)
            current_score = slideshow_score(current_output)

            if best_score < current_score:
                print('Found a better solution (+%s)' % (current_score - best_score))
                output = current_output
                best_score = current_score
            else:
                print(
                    'Better solution not found: %s (len: %s) < %s)' % (current_score, len(current_output), best_score))

        except KeyboardInterrupt:
            keep_going = False
            print()

    # Save result to output file only if better solution found
    if initial_best_score < best_score:
        print('Better solution found! (+%s)' % (best_score - initial_best_score))

        output_file = os.path.splitext(input_file)[0] + '.out'
        out_path = os.path.join(OUTPUT_DIRECTORY, output_file)

        write(output, out_path)
    else:
        print('No better solution found :(')
