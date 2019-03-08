import sys
import os
import random
import copy

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

from InputReader import InputReader
from write import write

from slide import Slide
from count import get_pics_per_tags

from score import get_current_best_score
from score import slideshow_score


def inverse_index_lookup_builder(pics, pics_per_tag, starting_node):
    current_node = starting_node

    path = []
    path.append(current_node)

    build_path = True
    while build_path:
        candidates = set()
        candidate_neighbours = {}

        # Delete current node and get next candidates
        for tag in pics[current_node].tags:
            pics_per_tag[tag].remove(current_node)
            candidates |= pics_per_tag[tag]

        # For each candidate, get remaining neighbour
        for candidate in candidates:
            candidate_neighbours[candidate] = set()
            for tag in pics[candidate].tags:
                candidate_neighbours[pics[candidate].id] |= pics_per_tag[tag]

        candidate_neighbours_count = {candidate: len(neighbour) for candidate, neighbour in
                                      candidate_neighbours.items()}

        # Get best next node
        current_node = None
        for candidate in candidates:
            if current_node is None:
                current_node = candidate
            # elif candidate_neighbours_count[candidate] == 1:
            #     current_node = candidate
            #     j += 1
            #     break
            elif candidate_neighbours_count[current_node] > candidate_neighbours_count[candidate]:
                current_node = candidate

        if current_node is None:
            build_path = False
        else:
            path.append(current_node)

    return path


if __name__ == '__main__':
    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    output_file = os.path.splitext(input_file)[0] + '.out'
    out_path = os.path.join(OUTPUT_DIRECTORY, output_file)

    # Get current best scores
    best_scores = get_current_best_score()
    initial_best_score = best_scores.get(input_file, 0)
    best_score = initial_best_score

    # Get objects from input file
    inputReader = InputReader(file_path)
    pics = inputReader.photos

    # Filter on horizontal pics
    pics = {k: v for k, v in pics.items() if v.orientation == 0}
    pics_id = list(pics.keys())

    print('Trying to sort %s H pics...' % len(pics_id))

    # Get pics per tag index
    pics_per_tag = get_pics_per_tags(pics)

    # Do better
    output = []

    print('Starting computation...')
    keep_going = True
    i = 0
    while keep_going:
        try:
            # copy working data structure
            current_pics_per_tag = copy.deepcopy(pics_per_tag)

            # Where to start from
            current_node = random.choice(pics_id)

            # Starting node neighbours
            starting_node_neighbours = set()
            for tag in pics[current_node].tags:
                starting_node_neighbours |= current_pics_per_tag[tag]

            # Make path
            forward_path = inverse_index_lookup_builder(pics, current_pics_per_tag, current_node)
            print('Found forward path of length %s' % len(forward_path))

            if len(forward_path) < 30000:
                continue

            # Go backwards to find another path
            backward_path = []
            for neighbour in starting_node_neighbours:
                if neighbour not in forward_path:
                    neighbour_pics_per_tag = copy.deepcopy(current_pics_per_tag)

                    current_backward_path = inverse_index_lookup_builder(pics, neighbour_pics_per_tag, neighbour)

                    if len(current_backward_path) > len(backward_path):
                        backward_path = current_backward_path

            print('Found backward path of length %s' % len(backward_path))
            backward_path.reverse()

            slideshow = []
            for id in backward_path + forward_path:
                slideshow.append(Slide(pics[id]))

            # Scoring current output
            current_score = slideshow_score(slideshow)

            if best_score < current_score:
                print()
                print('Found a better solution (+%s)' % (current_score - best_score))
                output = slideshow
                best_score = current_score

                write(output, out_path)
            else:
                print(
                    'Better solution not found: %s (len: %s) < %s)' % (current_score, len(slideshow), best_score))

        except KeyboardInterrupt:
            keep_going = False
            print()

    # Save result to output file only if better solution found
    if initial_best_score < best_score:
        print('Better solution found! (+%s)' % (best_score - initial_best_score))

    else:
        print('No better solution found :(')
