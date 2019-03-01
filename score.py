import os

from config import INPUT_DIRECTORY
from config import OUTPUT_DIRECTORY

from InputReader import InputReader
from slide import Slide


def transition_score(slide1, slide2):
    """
    Compute score between two Slides
    """
    tags_slide1 = slide1.tags
    tags_slide2 = slide2.tags
    common_tags = tags_slide1 & tags_slide2

    tags_only_slide1 = tags_slide1 - common_tags
    tags_only_slide2 = tags_slide2 - common_tags

    return min(len(tags_only_slide1), len(tags_only_slide2), len(common_tags))


def slideshow_score(list_slides):
    """
    Compute score of a slideshow represented as a list of slides
    """
    score = 0

    if len(list_slides) >= 2:
        score_sequence = [transition_score(list_slides[i], list_slides[i + 1]) for i in range(len(list_slides) - 1)]

        if 0 in score_sequence:
            score = -666
        else:
            score = sum([transition_score(list_slides[i], list_slides[i + 1]) for i in range(len(list_slides) - 1)])

    return score


def get_current_best_score():
    best_scores = {}

    for output_filename in os.listdir(OUTPUT_DIRECTORY):
        # Read input
        input_filename = '%s.txt' % os.path.splitext(output_filename)[0]
        reader = InputReader(os.path.join(INPUT_DIRECTORY, input_filename))
        pics = reader.photos

        try:

            # Retrieve output
            with open(os.path.join(OUTPUT_DIRECTORY, output_filename)) as f:
                header = f.readline()

                output_ids = []
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        output_ids.append(int(line))

            # Recreate solution
            output = []
            for id in output_ids:
                output.append(Slide(pics[id]))

            # Score solution
            current_score = slideshow_score(output)
        except KeyError:
            current_score = -1

        best_scores[input_filename] = current_score

    return best_scores


if __name__ == '__main__':
    best_scores = get_current_best_score()

    total_score = 0
    for filename, score in best_scores.items():
        print('%s score: %s' % (filename, score))
        total_score += score

    print('===> total score: %s' % total_score)
