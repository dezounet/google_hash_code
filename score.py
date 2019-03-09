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

    tags_only_slide1_count = len(tags_slide1) - len(common_tags)
    tags_only_slide2_count = len(tags_slide2) - len(common_tags)

    return min(tags_only_slide1_count, tags_only_slide2_count, len(common_tags))


def slideshow_score(list_slides):
    """
    Compute score of a slideshow represented as a list of slides
    """
    score = 0

    if len(list_slides) >= 2:
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

                output = []
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        pic_1_2 = line.split(' ')

                        pic_1 = pics[int(pic_1_2[0])]
                        if len(pic_1_2) > 1:
                            pic_2 = pics[int(pic_1_2[1])]
                        else:
                            pic_2 = None

                        output.append(Slide(pic_1, pic_2))

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
