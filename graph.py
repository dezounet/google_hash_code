from slide import Slide
from score import transition_score


class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.uid] = node

    def add_link(self, uid_1, uid_2):
        node_1 = self.nodes[uid_1]
        node_2 = self.nodes[uid_2]

        node_1.add_neighbour(node_2)

    def del_link(self, uid_1, uid_2):
        node_1 = self.nodes[uid_1]
        node_2 = self.nodes[uid_2]

        node_1.del_neighbour(node_2)

    def remove_node(self, uid):

        neighbours_uid = []
        for neighbour_uid, neighbour in self.nodes[uid].neighbours.items():
            # Do not edit inplace
            neighbours_uid.append(neighbour_uid)

        for neighbour_uid in neighbours_uid:
            self.del_link(uid, neighbour_uid)
            self.del_link(neighbour_uid, uid)

    def get_best_neighbour(self, uid):
        node = self.nodes[uid]

        best_neighbour = None
        for neighbour_uid, neighbour in node.neighbours.items():
            if best_neighbour is None:
                best_neighbour = neighbour
            elif best_neighbour.weight < neighbour.weight and \
                    len(neighbour.node.neighbours) > 0:
                best_neighbour = neighbour
            elif best_neighbour.weight == neighbour.weight and \
                    len(neighbour.node.neighbours) > len(best_neighbour.node.neighbours):
                best_neighbour = neighbour

        if best_neighbour is not None:
            best_neighbour = best_neighbour.node.uid

        return best_neighbour


class Node(object):
    def __init__(self, uid, slide):
        self.uid = uid
        self._slide = slide

        self.neighbours = {}

    def get_slide(self):
        return self._slide

    def add_neighbour(self, node):
        if node.uid not in self.neighbours:
            self.neighbours[node.uid] = Neighbour(self, node)

    def del_neighbour(self, node):
        if node.uid in self.neighbours:
            del self.neighbours[node.uid]


class Neighbour(object):
    def __init__(self, current_node, neighbour_node):
        self.node = neighbour_node

        self.weight = transition_score(current_node.get_slide(), neighbour_node.get_slide())


def build_graph(pics, pics_per_tag):
    graph = Graph()

    # Add node to graph
    print('Adding nodes to graph...')
    for uid, pic in pics.items():
        node = Node(uid, Slide(pic))
        graph.add_node(node)
    print('Nodes added to graph.')

    # Link nodes in graph
    print('Adding links to graph...')
    for tag, tag_pics in pics_per_tag.items():
        for pic_id_1 in tag_pics:
            pic_1 = pics[pic_id_1]

            for pic_id_2 in tag_pics:
                pic_2 = pics[pic_id_2]

                if pic_id_1 != pic_id_2:
                    graph.add_link(pic_1.id, pic_2.id)
    print('Links added to graph.')

    return graph


def crawl_graph(graph, starting_node_uid):
    path = []
    current_node_uid = starting_node_uid

    keep_going = True
    while keep_going:
        next_node_uid = graph.get_best_neighbour(current_node_uid)

        if next_node_uid is None:
            keep_going = False
        else:
            # Cannot move backward to selected node
            graph.remove_node(current_node_uid)

            current_node_uid = next_node_uid
            path.append(current_node_uid)

    return path
