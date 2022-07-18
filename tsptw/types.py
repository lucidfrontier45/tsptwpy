from dataclasses import dataclass
from typing import Callable, TypeAlias

time_t: TypeAlias = float
TravelTimeFunc = Callable[[int, int], time_t]


@dataclass(frozen=True)
class Requirement:
    ta: time_t
    td: time_t
    op: time_t
    wt: time_t


RequirementFunc = Callable[[int], Requirement]


def calc_node_times(
    p_city_id: int,
    p_td: time_t,
    city_id: int,
    req: Requirement,
    T: TravelTimeFunc,
):
    ta = p_td + T(p_city_id, city_id)
    if ta < req.ta:
        ta = min(ta + req.wt, req.ta)
    td = ta + req.op
    return ta, td


@dataclass(frozen=True)
class Node:
    city_id: int
    parents: list[int]
    children: list[int]
    ta: time_t
    td: time_t

    @classmethod
    def from_parent(
        cls, parent: "Node", city_id: int, req: Requirement, T: TravelTimeFunc
    ):
        parent_nodes = parent.parents + [parent.city_id]
        child_nodes = list(parent.children)
        child_nodes.remove(city_id)
        ta, td = calc_node_times(parent.city_id, parent.td, city_id, req, T)
        return cls(city_id, parent_nodes, child_nodes, ta, td)

    def is_leaf(self):
        return len(self.children) == 0

    def validate(self, req: Requirement):
        return self.ta >= req.ta and self.td <= req.td

    def generate_child_nodes(
        self, R: RequirementFunc, T: TravelTimeFunc, only_valid=True
    ):
        child_nodes: list[Node] = []
        for c in self.children:
            req = R(c)
            node = Node.from_parent(self, c, req, T)
            if only_valid and not node.validate(req):
                continue
            child_nodes.append(node)
        return child_nodes


NodeEvaluator = Callable[[Node, int, int, RequirementFunc, TravelTimeFunc], time_t]
