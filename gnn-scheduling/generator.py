import numpy as np
import pandas as pd
from estee.common import DataObject, TaskGraph
from estee.generators.utils import normal
from estee.schedulers import BlevelGtScheduler
from estee.simulator import MaxMinFlowNetModel, Simulator, Worker


def merge_neighbours(count):
    g = TaskGraph()

    tasks1 = [g.new_task("a{}".format(i), duration=normal(15, 3),
                         expected_duration=15,
                         outputs=[DataObject(normal(99, 2.5), 100)])
              for i in range(count)]
    for i in range(count):
        t = g.new_task("b{}".format(i), duration=normal(15, 2), expected_duration=15)
        t.add_input(tasks1[i])
        t.add_input(tasks1[(i + 1) % count])
    return g


def simulate_graph(graph: TaskGraph):
    scheduler = BlevelGtScheduler()
    workers = [Worker(cpus=1) for _ in range(1)]
    netmodel = MaxMinFlowNetModel(bandwidth=100)
    simulator = Simulator(graph, workers, scheduler, netmodel)

    return simulator.run()


def generate_dataset_1(count=100):
    np.random.seed(0)
    graphs = []
    makespans = []

    for i in range(count):
        graph = merge_neighbours(10)
        graphs.append(graph)
        makespans.append(simulate_graph(graph))
    return pd.DataFrame({
        "graph": graphs,
        "makespan": makespans
    })
