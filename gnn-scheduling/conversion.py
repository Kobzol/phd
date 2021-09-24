from collections import deque
from itertools import chain

import networkx as nx
import torch
from estee.common import TaskGraph

from data import TrainExample


def estee_to_pyg(example: TrainExample):
    """
    Returns (node_features, edge_index)
    """
    graph = example.graph
    edges_from = []
    edges_to = []
    features = [None] * len(graph.tasks)

    to_visit = deque(graph.source_tasks())
    visited = set()
    while to_visit:
        node = to_visit.popleft()
        if node in visited:
            continue
        visited.add(node)
        consumers = list(chain.from_iterable(o.consumers for o in node.outputs))
        feats = [node.duration, example.worker_count]
        features[node.id] = feats
        for consumer in consumers:
            if consumer not in visited:
                edges_from.append(node.id)
                edges_to.append(consumer.id)
                to_visit.append(consumer)

    assert len(edges_from) == len(edges_to)
    edge_index = torch.tensor([edges_from, edges_to], dtype=torch.long)

    node_features = torch.tensor(features, dtype=torch.float)

    return node_features, edge_index


def estee_to_nx(graph: TaskGraph) -> nx.DiGraph:
    nx_graph = nx.DiGraph()
    for task in graph.tasks.values():
        for output in task.outputs:
            nx_graph.add_edge(f"t{task.id}", f"o{output.id}")
            for next_task in output.consumers:
                nx_graph.add_edge(f"o{output.id}", f"t{next_task.id}")
    return nx_graph
