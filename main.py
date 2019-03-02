import sys
import os
import random

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

from InputReader import InputReader
from write import write

from slide import Slide
from count import get_pics_per_tags

from graph import build_graph
from graph import crawl_graph

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

    # Filter on horizontal pics
    # TODO: replace this by a vertical merge function
    pics = {k: v for k, v in pics.items() if v.orientation == 0}
    pics_id = list(pics.keys())

    # Get pics per tag index
    pics_per_tag = get_pics_per_tags(pics)

    # Do better
    output = []

    print('Starting computation...')
    keep_going = True
    i = 0
    while keep_going:
        try:
            # Minimalistic progress bar
            print('.', end='', flush=True)
            if i % 100 == 0 and i != 0:
                print()
            i += 1

            current_output = []

            # Build graph
            graph = build_graph(pics, pics_per_tag)

            starting_node = random.choice(pics_id)
            path = crawl_graph(graph, starting_node)

            for uid in path:
                current_output.append(Slide(pics[uid]))

            current_score = slideshow_score(current_output)

            if best_score < current_score:
                print()
                print('Found a better solution (+%s)' % (current_score - best_score))
                output = current_output
                best_score = current_score

        except KeyboardInterrupt:
            keep_going = False
            print()

    # Save result to output file only if better solution found
    if initial_best_score < best_score:
        print('Better solution found! (%s)' % (best_score - initial_best_score))

        output_file = os.path.splitext(input_file)[0] + '.out'
        out_path = os.path.join(OUTPUT_DIRECTORY, output_file)

        write(output, out_path)
    else:
        print('No better solution found :(')
