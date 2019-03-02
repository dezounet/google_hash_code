import sys
import os
import math

from collections import Counter

if __name__ == '__main__':

    from config import INPUT_DIRECTORY
    from config import DESC_DIRECTORY

    from InputReader import InputReader


    def write_desc(counter, filename):
        count = sum(count for n, count in counter.items())
        sum_of_numbers = sum(number * count for number, count in counter.items())
        mean = sum_of_numbers / count

        total_squares = sum(number * number * count for number, count in counter.items())
        mean_of_squares = total_squares / count
        variance = mean_of_squares - mean * mean
        std_dev = math.sqrt(variance)

        best_mean_score = mean / 3
        max_score = best_mean_score * sum_of_numbers

        with open(filename, 'w') as f:
            f.write('%s %s %s %s\n' % (mean, std_dev, best_mean_score, max_score))
            for tag, count in sorted(counter.most_common(), key=lambda x: x[0]):
                f.write('%s %s\n' % (tag, count))


    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    # Get objects from input file
    inputReader = InputReader(file_path)

    occurrences = []
    for i, pic in inputReader.photos.items():
        occurrences.append(len(pic.tags))

    counter = Counter(occurrences)

    # Save result to output file
    output_file = os.path.splitext(input_file)[0] + '.count'
    out_path = os.path.join(DESC_DIRECTORY, output_file)

    write_desc(counter, out_path)
