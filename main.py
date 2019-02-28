import sys
import os

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

from read import read
from write import write


if __name__ == '__main__':
    # Get input file from command line arg list
    input_file = sys.argv[1]
    file_path = os.path.join(INPUT_DIRECTORY, input_file)
    assert os.path.exists(file_path)

    # Get objects from input file
    input = read(file_path)

    # TODO

    # Save result to output file
    output_file = os.path.splitext(input_file)[0] + '.out'
    out_path = os.path.join(OUTPUT_DIRECTORY, output_file)

    write(out_path)
