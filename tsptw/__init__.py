from typing import Optional

from .types import Node, Requirement, RequirementFunc, TravelTimeFunc, calc_node_times


def simple_evaluation(
    node: Node, start: int, end: int, R: RequirementFunc, T: TravelTimeFunc
):
    return node.td


def heuristic_evaluation(
    node: Node, start: int, end: int, R: RequirementFunc, T: TravelTimeFunc
):
    p_city_id, td = (node.city_id, node.td)

    def sort_func(c_r: tuple[int, Requirement]):
        req = c_r[1]
        return req.td - req.op

    remained = sorted(((c, R(c)) for c in node.children), key=sort_func)

    for (city_id, req) in remained:
        _, td = calc_node_times(p_city_id, td, city_id, req, T)
        p_city_id = city_id

    return td + T(p_city_id, end)


def solve(
    start: int,
    end: int,
    cities: list[int],
    R: RequirementFunc,
    T: TravelTimeFunc,
):
    # initialization
    root_node = Node(start, [], cities, 0.0, 0.0)
    V: list[Node] = [root_node]
    best_score = 1.0e10
    best_node: Optional[Node] = None

    # loop until V becomes empty
    while len(V) > 0:
        n = V.pop()

        if n.is_leaf():
            score = n.td + T(n.city_id, end)
            if score < best_score:
                best_score = score
                best_node = n
            continue

        # branch
        child_nodes = n.generate_child_nodes(R, T, only_valid=True)
        # bound
        child_nodes = [
            cn
            for cn in child_nodes
            if heuristic_evaluation(cn, start, end, R, T) < best_score
        ]

        V.extend(child_nodes)

    # finalization
    if best_node is None:
        return None

    path = best_node.parents + [best_node.city_id, end]
    return path, best_score
