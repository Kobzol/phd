from estee.common import DataObject, TaskGraph
from estee.generators.utils import normal
from estee.schedulers import BlevelGtScheduler
from estee.simulator import Simulator, Worker
from estee.simulator.netmodels import InstantNetModel

from .data import TrainExample


def merge_neighbours(count, normal_center=20):
    g = TaskGraph()

    tasks1 = [g.new_task("a{}".format(i), duration=normal(normal_center * 1.2, normal_center / 4),
                         expected_duration=15,
                         outputs=[DataObject(normal(99, 2.5), 100)])
              for i in range(count)]
    for i in range(count):
        t = g.new_task("b{}".format(i), duration=normal(normal_center, normal_center / 4),
                       expected_duration=15)
        t.add_input(tasks1[i])
        t.add_input(tasks1[(i + 1) % count])
    return g


def triplets(count, cpus):
    g = TaskGraph()
    for i in range(count):
        t1 = g.new_task("a{}".format(i), duration=normal(5, 1.5), expected_duration=5,
                        output_size=40)
        t2 = g.new_task("b{}".format(i), duration=normal(120, 20), expected_duration=120,
                        output_size=120, cpus=cpus)
        t2.add_input(t1)
        t3 = g.new_task("c{}".format(i), duration=normal(32, 3), expected_duration=32)
        t3.add_input(t2)
    return g


def simulate_graph(example: TrainExample):
    netmodel = InstantNetModel()

    scheduler = BlevelGtScheduler()
    workers = [Worker(cpus=1) for _ in range(example.worker_count)]
    simulator = Simulator(example.graph, workers, scheduler, netmodel)

    return simulator.run()
