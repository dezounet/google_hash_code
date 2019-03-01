from photo import Photo;
import collections;


class InputReader:
    photos = {}

    # tags_counter = collections.Counter();
    # orientation_counter = collections.Counter();

    def __init__(self, path: str) -> None:
        # print(f'Read input {path}')

        file = open(path, 'r')

        photo_id = 0
        first_line = True
        for line in file:
            line = line.strip()

            # print(line)
            if first_line:
                first_line = False
            else:
                line_splited = list(line.split(' '))

                orientation_line = line_splited.pop(0)
                orientation = 0
                if orientation_line == 'V':
                    orientation = 1

                number_tags = line_splited.pop(0)
                tags = set(line_splited)
                self.photos[photo_id] = Photo(photo_id, orientation, tags)
                photo_id += 1

                # self.orientation_counter[orientation] += 1
                # for tag in tags:
                #    self.tags_counter[tag] += 1

        file.close()
