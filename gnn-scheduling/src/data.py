import dataclasses

from estee.common import TaskGraph


@dataclasses.dataclass()
class TrainExample:
    graph: TaskGraph
    worker_count: int
