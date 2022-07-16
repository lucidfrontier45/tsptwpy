from typing import Optional

from .types import Node, RequirementFunc, TravelTimeFunc


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
        child_nodes = [cn for cn in child_nodes if cn.td < best_score]

        V.extend(child_nodes)

    # finalization
    if best_node is None:
        return None

    path = best_node.parents + [best_node.city_id, end]
    return path, best_score
