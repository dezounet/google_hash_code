from slide import Slide
from score import transition_score


class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.max_recursion = 4

    def set_max_recursion(self, max_recursion):
        self.max_recursion = max_recursion

    def get_max_recursion(self):
        return self.max_recursion

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
        best_neighbour_reachable_nodes = 0
        for neighbour_uid, neighbour in node.neighbours.items():
            if best_neighbour is None:
                best_neighbour = neighbour
                best_neighbour_reachable_nodes = self.get_reachable_node(best_neighbour.node.uid)
            # elif len(neighbour.node.neighbours) == 2:
            #    # If a neighbour only has another neighbour, do not leave him alone!
            #    best_neighbour = neighbour
            #    break
            elif len(self.get_reachable_node(neighbour.node.uid)) > len(
                    best_neighbour_reachable_nodes):
                best_neighbour = neighbour
                best_neighbour_reachable_nodes = self.get_reachable_node(best_neighbour.node.uid)

        if best_neighbour is not None:
            best_neighbour = best_neighbour.node.uid

        return best_neighbour

    def get_reachable_node(self, uid, max_recursion=None, ignored_nodes=None):
        reachable_nodes = set()

        if max_recursion is None:
            max_recursion = self.get_max_recursion()

        if ignored_nodes is None:
            ignored_nodes = set()

        starting_node = self.nodes[uid]

        reachable_nodes.add(starting_node)
        ignored_nodes.add(starting_node)

        if max_recursion <= 0:
            return reachable_nodes

        for neighbour_uid, neighbour in starting_node.neighbours.items():
            if neighbour_uid in ignored_nodes:
                continue
            else:
                reachable_nodes |= self.get_reachable_node(neighbour_uid,
                                                           max_recursion=(max_recursion - 1),
                                                           ignored_nodes=ignored_nodes)

        return reachable_nodes

    def break_links(self, filter_fn):
        links_to_del = []

        for node_uid, node in self.nodes.items():
            for neighbour_uid, neighbour in node.neighbours.items():
                if not filter_fn(node, neighbour):
                    links_to_del.append((node_uid, neighbour_uid))

        for node_uid, neighbour_uid in links_to_del:
            self.del_link(node_uid, neighbour_uid)

    def count_links(self):
        link_count = 0
        for node_uid, node in self.nodes.items():
            link_count += len(node.neighbours)

        return link_count

    def clean_dead_end(self):
        dead_end = []

        for uid, node in self.nodes.items():
            if len(node.neighbours) == 1:
                dead_end.append(uid)

        for uid in dead_end:
            self.remove_node(uid)


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
    for uid, pic in pics.items():
        node = Node(uid, Slide(pic))
        graph.add_node(node)

    # Link nodes in graph
    for tag, tag_pics in pics_per_tag.items():
        for pic_id_1 in tag_pics:
            pic_1 = pics[pic_id_1]

            for pic_id_2 in tag_pics:
                pic_2 = pics[pic_id_2]

                if pic_id_1 != pic_id_2:
                    graph.add_link(pic_1.id, pic_2.id)

    return graph


def crawl_graph(graph, starting_node_uid, recursion_strategy=None):
    if recursion_strategy is None:
        recursion_strategy = {
            0: 2,
            5000: 2,
            15000: 3,
            20000: 4,
            25000: 5,
            30000: 6,
            35000: 7,
            40000: 8,
            45000: 9,
        }

    path = []
    current_node_uid = starting_node_uid
    path.append(current_node_uid)

    keep_going = True
    i = 0
    while keep_going:
        if i % 10 == 0:
            # remove dead end node
            # graph.clean_dead_end()
            pass

        if i % 2000 == 0:
            print('looking for node %s' % i)
            from collections import Counter
            occurrences = []
            for uid, node in graph.nodes.items():
                occurrences.append(len(node.neighbours))

            # counter = Counter(occurrences)
            # print('%s (path) -> %s' % (len(path), sorted(counter.most_common(), key=lambda x: x[0])))

        # update recursion strategy
        if i in recursion_strategy:
            graph.set_max_recursion(recursion_strategy[i])

        next_node_uid = graph.get_best_neighbour(current_node_uid)

        if next_node_uid is None:
            keep_going = False
        else:
            # Cannot move backward to selected node
            graph.remove_node(current_node_uid)

            current_node_uid = next_node_uid
            path.append(current_node_uid)

        i += 1

    return path
