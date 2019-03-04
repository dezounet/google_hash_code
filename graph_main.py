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
            current_output = []

            # Build graph
            graph = build_graph(pics, pics_per_tag)
            print('graph link count (before filtering): %s' % graph.count_links())
            graph.break_links(lambda x, y: y.weight >= 1)
            print('graph link count (after filtering): %s' % graph.count_links())

            starting_node = random.choice(pics_id)
            starting_node_neighbours = [uid for uid, n in graph.nodes[starting_node].neighbours.items()]

            # Go as far as possible
            path = crawl_graph(graph, starting_node)

            # trying to extend the initial path, going the other way
            reverse_path = []
            for node_uid in starting_node_neighbours:
                a_reverse_path = crawl_graph(graph, node_uid, recursion_strategy={0: 8})

                if len(reverse_path) < len(a_reverse_path):
                    reverse_path = a_reverse_path

            # Reverse as we've crawled it backward
            reverse_path.reverse()

            print('Completing the forward path with backward crawling: +%s' % len(reverse_path))
            for uid in reverse_path + path:
                current_output.append(Slide(pics[uid]))

            current_score = slideshow_score(current_output)

            if best_score < current_score:
                print()
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
