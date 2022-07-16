from tsptw.types import Node, Requirement, time_t

travel_time_matrix: list[list[time_t]] = [
    [0.0, 1.0, 2.0, 5.0, 3.0],
    [1.0, 0.0, 3.0, 7.0, 4.0],
    [2.0, 3.0, 0.0, 4.0, 2.0],
    [5.0, 7.0, 4.0, 0.0, 1.0],
    [3.0, 4.0, 2.0, 1.0, 0.0],
]


def travel_time_func(city_from: int, city_to: int):
    return travel_time_matrix[city_from][city_to]


def test_create_from_parent():
    parent_node = Node(1, [0], [2, 3], 3.0, 4.0)

    req = Requirement(0.0, 10.0, 1.0, 2.0)
    child_node = Node.from_parent(parent_node, 2, req, travel_time_func)
    assert child_node == Node(2, [0, 1], [3], 7.0, 8.0)

    req = Requirement(8.0, 10.0, 1.0, 2.0)
    child_node = Node.from_parent(parent_node, 2, req, travel_time_func)
    assert child_node == Node(2, [0, 1], [3], 8.0, 9.0)

    req = Requirement(15.0, 20.0, 1.0, 2.0)
    child_node = Node.from_parent(parent_node, 2, req, travel_time_func)
    assert child_node == Node(2, [0, 1], [3], 9.0, 10.0)


def test_validate_node():
    node = Node(1, [0], [2, 3], 3.0, 4.0)

    req = Requirement(0.0, 10.0, 1.0, 1.0)
    assert node.validate(req)

    req = Requirement(4.0, 10.0, 1.0, 1.0)
    assert not node.validate(req)

    req = Requirement(0.0, 3.0, 1.0, 1.0)
    assert not node.validate(req)


def test_node_from_root():
    start = 0
    end = 4

    root_node = Node(0, [], [1, 2, 3], 0, 0)

    req = Requirement(0.0, 4.0, 1, 1)
    nodes = root_node.generate_child_nodes(lambda c: req, travel_time_func, True)
    nodes.sort(key=lambda node: node.city_id)
    correct_nodes = [
        Node(1, [0], [2, 3], 1.0, 2.0),
        Node(2, [0], [1, 3], 2.0, 3.0),
    ]

    assert len(nodes) == len(correct_nodes)
    for (n, cn) in zip(nodes, correct_nodes):
        assert n == cn
