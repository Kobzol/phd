import dataclasses
import functools
from typing import Iterable, List, Optional, Union

from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.ext.list import ListBuilder

from tasks import cluster_1, get_task_color, half_node, node, task, \
    task_graph_grid
from utils import github_link, quotation, slide_header_top


@dataclasses.dataclass
class SlurmEntry:
    label: str = ""
    state: str = ""
    color: Optional[str] = None


class SlurmQueue:
    def __init__(self, box: Box, entries: int, width=200, height=60):
        self.box = box.box(width=width, height=height * entries)
        self.width = width
        self.height = height

        self.set_state([SlurmEntry() for _ in range(entries)], show="1+")

    def set_state(self, entries: List[SlurmEntry], show: str) -> List[Box]:
        wrapper = self.box.overlay(show=show)
        boxes = []

        ratio = 0.75
        for (index, entry) in enumerate(entries):
            entry_box = wrapper.box(width=self.width, height=self.height, y=index * self.height,
                                    horizontal=True)
            label_box = entry_box.box(width=self.width * ratio, height=self.height)
            label_box.rect(color="black", bg_color="white")
            label_box.text(entry.label)
            state_box = entry_box.box(width=(1.0 - ratio) * self.width, height=self.height)
            state_box.rect(color="black", bg_color="white")
            state_box.text(entry.state)
            boxes.append(entry_box)

        for (entry, box) in zip(entries, boxes):
            if entry.color is not None:
                box.overlay(show=show, z_level=2).rect(color=entry.color, stroke_width=4)
        return boxes


def create_empty_task_fn(task_size: int):
    def empty_task(box, x, y, name, size, row, col):
        return box.box(x=x - task_size / 2, y=y - task_size / 2, width=task_size,
                       height=task_size)

    return empty_task


def hyperqueue(slides: Slides):
    @slides.slide()
    def hq_intro(slide: Box):
        rows = slide.box(x=50, horizontal=True)
        paper_box = rows.box(p_right=40).box(width=400)
        paper_box.rect(color="black", stroke_width=4)
        paper_box.image("images/hq-paper.png")

        box = rows.box(y=0)
        box.box().text("HyperQueue: Efficient and ergonomic\ntask graphs on HPC clusters")
        size = 30
        box.box(p_top=20).text("Jakub Beránek, Ada Böhm, Gianluca Palermo, Jan Martinovič, Branislav Jansík", style=T(size=size))
        box.box().text("(SoftwareX 2024)", style=T(size=size))

        box.update_style("default", T(size=40))
        lst = unordered_list(box.box(p_top=60))
        lst.item(show="next+").text("How to deal with HPC workflow challenges?")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Interaction with HPC allocation managers", style="l2")
        lst2.item(show="next+").text("Heterogeneous resource management", style="l2")
        lst2.item(show="next+").text("Scalability", style="l2")
        lst.item(show="next+").text("Can we integrate the solutions into a single task runtime?")

    @slides.slide()
    def task_to_allocation_mapping(slide: Box):
        content = slide_header_top(slide, "Challenge: how to map tasks to allocations?")
        content.update_style("default", T(size=50))
        content.update_style("l2", T(size=30))

        lst = unordered_list(content.box(x=50, p_top=100))
        lst.item(show="next+").text("Each task is a separate allocation")
        lst2 = lst.ul()
        lst2.item().text("Massive overhead (millions of allocations)", style="l2")
        lst2.item().text("Allocation count limits", style="l2")
        lst2.item().text("Node granularity", style="l2")
        lst2.item().text("Difficult with dependencies", style="l2")
        lst.item(show="next+", p_top=10).text("One allocation for the whole task graph")
        lst2 = lst.ul()
        lst2.item().text("Only for small task graphs", style="l2")
        lst2.item().text("Leads to resource waste", style="l2")
        lst.item(show="next+", p_top=10).text("Split task graph into multiple allocations")
        lst2 = lst.ul()
        lst2.item().text("Challenging to find good partitioning", style="l2")
        lst2.item().text("No load balancing across allocations", style="l2")

        task_size = 50
        node_size = 60

        def task_fn(box, x, y, name, size, row, col):
            return task(box, x=x, y=y, name=None, size=size, bg_color=get_task_color(col))

        def tg(box: Box, color=None):
            return task_graph_grid(box, size=task_size, rows=1, cols=3, task_constructor=task_fn)

        x_start = 1100
        y_start = 160
        y_offset = 240

        # Each task as a job
        box_1 = content.box(x=x_start, y=y_start, horizontal=True, show="2+")
        tasks = tg(box_1.box(p_right=40))

        def get_color(index: int) -> str:
            if index == 0:
                return "black"
            return get_task_color(index + 2)

        for (index, task_box) in enumerate(tasks):
            task(box=task_box, x=task_size / 2, y = task_size / 2, size=task_size,
                 bg_color=get_task_color(index), color=get_color(index))
        nodes = cluster_1(box_1.box(), size=node_size)
        for (index, node_box) in enumerate(nodes[:3]):
            node(node_box.overlay(z_level=2), x=node_size / 2, y=node_size / 2, size=node_size,
                 bg_color=get_task_color(index), color=get_color(index),
                 node_args=dict(stroke_width=4))

        # Task graph as a single job
        box_1 = content.box(x=x_start, y=y_start + y_offset, horizontal=True, show="3+")
        tg(box_1.box(p_right=40))
        nodes = cluster_1(box_1.box(), size=node_size)
        node_box = nodes[0]
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(0))
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(1), mode="down")
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(2), mode="left")
        node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
             bg_color=None, node_args=dict(stroke_width=4))

        # Split graph
        box_1 = content.box(x=x_start, y=y_start + y_offset * 2, horizontal=True, show="4+")
        tasks = tg(box_1.box(p_right=40))
        task(box=tasks[2].overlay(), x=task_size / 2, y=task_size / 2, size=task_size,
             bg_color=get_task_color(2), color=get_task_color(3))

        nodes = cluster_1(box_1.box(), size=node_size)
        node_box = nodes[0]
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(0))
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(1), mode="down")
        node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
             bg_color=None, node_args=dict(stroke_width=4))
        node(nodes[1].overlay(z_level=2), x=node_size / 2, y=node_size / 2, size=node_size,
             bg_color=get_task_color(2), node_args=dict(stroke_width=4), color=get_task_color(3))

    # @slides.slide()
    # def hq_approach(slide: Box):
    #     slide.box().text("HyperQueue meta-scheduling approach")
    #     slide.box(show="next+", p_top=80).text("Disentangle what to compute (tasks) +")
    #     slide.box(show="next+").text("where to compute it (nodes)")

    @slides.slide()
    def metascheduling(slide: Box):
        content = slide_header_top(slide, "Task graph partitioning")
        content.update_style("default", T(size=42))

        margin_bottom = 30
        margin_line = 15

        wrapper = content.box(y=160)

        width = 700
        row = wrapper.box(horizontal=True, p_bottom=margin_bottom, width=width, height=160,
                          show="next+")

        label_size = 34
        content.box(x=50, y=row.y("50%").add(-20), show="2+").text("Manual (Slurm)",
                                                                   style=T(size=label_size))

        node_size = 40
        task_size = 40

        def pbs_task(offset: int, box, x, y, name, size, row, col):
            bg_color = get_task_color(col + offset)
            return task(box=box, x=x, y=y, name=None, size=size, bg_color=bg_color)

        def node_row(box: Box, count: int):
            margin = node_size * 0.2
            row = box.box(horizontal=True, width=node_size * count + margin * (count - 1),
                          height=node_size)
            x = node_size / 2
            for _ in range(count):
                node(row.box(width=node_size, x=x), size=node_size)
                x += node_size + margin

        task_box = row.box()
        task_box_1 = task_box.fbox(show="2-3")
        task_graph_grid(task_box_1.box(), size=task_size, rows=1, cols=3,
                        task_constructor=functools.partial(pbs_task, offset=0))
        task_box_1.box().text("+", style=T(size=30))
        node_row(task_box_1.box(), count=3)

        task_box_2 = task_box.overlay(show="4+")
        task_graph_grid(task_box_2.box(), size=task_size, rows=1, cols=2,
                        task_constructor=functools.partial(pbs_task, offset=3))
        task_box_2.box().text("+", style=T(size=30))
        node_row(task_box_2.box(), count=1)

        row.box(p_left=250, p_right=250).text("→ Slurm →")

        def overlay_node(node_box: Box, show: str,
                         color_index: Optional[Union[int, str]] = None,
                         mode="full"):
            box = node_box.overlay()
            modes = {
                "full": node,
                "up": lambda **args: half_node(mode="up", **args),
                "down": lambda **args: half_node(mode="down", **args)
            }

            stroke_width = 6 if mode == "full" else 4
            modes[mode](box=box, x=node_size / 2, y=node_size / 2, size=node_size,
                        bg_color=get_task_color(color_index) if color_index is not None else None,
                        show=show, node_args=dict(stroke_width=stroke_width))
            if mode != "full":
                node(box=box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                     show=show, node_args=dict(stroke_width=4))

        pbs_nodes = cluster_1(row.box(x=row.x("100%").add(-25)), size=node_size)
        for i in range(3):
            overlay_node(pbs_nodes[i], show="3+", color_index=i)
        overlay_node(pbs_nodes[3], show="5+", color_index=3, mode="up")
        overlay_node(pbs_nodes[3], show="5+", color_index=4, mode="down")

        content.overlay(show="next+", p_bottom=margin_bottom).line((
            (content.x("5%"), row.y("100%").add(margin_line)),
            (content.x("95%"), row.y("100%").add(margin_line))
        ))

        row = wrapper.box(horizontal=True, width=width, height=300, show="last+")

        content.box(x=50, y=row.y("[50%]").add(-20), show="last+").text("Meta-scheduling",
                                                                      style=T(size=label_size))

        task_box = row.box()
        fragment = slide.current_fragment()
        task_box_1 = task_box.fbox(show=f"{fragment}-{fragment + 2}")
        task_graph_grid(task_box_1.box(), size=task_size, rows=1, cols=3,
                        task_constructor=functools.partial(pbs_task, offset=0))

        text_box = row.box(p_left=20, p_right=100, horizontal=True)
        text_box.box(p_right=20).text("→")
        text_box.box().text("Meta-scheduler")

        slurm_box_width = 200
        slurm_box = text_box.box(p_left=20, width=slurm_box_width).text("→ Slurm →")
        below_slurm_box = row.box(x=slurm_box.x(0), y=slurm_box.y("100%"), width=slurm_box_width,
                                show=f"{fragment + 1}+")
        below_slurm_box.box().text("↑")
        node_row(below_slurm_box.box(), count=2)

        pbs_nodes = cluster_1(row.box(x=row.x("100%").add(-25)), size=node_size)
        node_fragment = f"{fragment + 2}+"
        overlay_node(pbs_nodes[0], show=node_fragment, color_index=0, mode="up")
        overlay_node(pbs_nodes[0], show=node_fragment, color_index=1, mode="down")
        overlay_node(pbs_nodes[1], show=node_fragment, color_index=2)

        task_box_2 = task_box.overlay(show=f"{fragment + 3}+")
        task_graph_grid(task_box_2.box(), size=task_size, rows=1, cols=2,
                        task_constructor=functools.partial(pbs_task, offset=3))

        overlay_node(pbs_nodes[0], show=f"{fragment + 4}+", color_index=3, mode="down")
        overlay_node(pbs_nodes[1], show=f"{fragment + 4}+", color_index=4)

        content.overlay(show="next+", p_bottom=margin_bottom).line((
            (content.x("5%"), row.y("100%").add(margin_line)),
            (content.x("95%"), row.y("100%").add(margin_line))
        ))

        row = wrapper.box(horizontal=True, width=width, height=300, show="last+")

        content.box(x=50, y=row.y("[50%]").add(-40), show="last+").text("Meta-scheduling +\nautomatic allocation",
                                                                      style=T(size=label_size))

        task_box = row.box()
        task_graph_grid(task_box.box(), size=task_size, rows=1, cols=3,
                        task_constructor=functools.partial(pbs_task, offset=0))

        text_box = row.box(p_left=20, p_right=100, horizontal=True)
        text_box.box(p_right=20).text("→")
        hq_box = text_box.box().text("Meta-scheduler")
        text_box.box(p_left=20, width=slurm_box_width).text("→ Slurm →")

        pbs_nodes = cluster_1(row.box(x=row.x("100%").add(-25)), size=node_size)

        node(row.box(x=hq_box.x("50%"), y=hq_box.y(0).add(-25), show="next+"), x=0, y=0,
             size=node_size, node_args=dict(stroke_dasharray="4", stroke_width="2"))

        fragment = slide.current_fragment() + 1
        overlay_node(pbs_nodes[0], show=f"{fragment}", color_index=None)
        overlay_node(pbs_nodes[1], show=f"{fragment}", color_index=None)
        overlay_node(pbs_nodes[0], show=f"{fragment + 1}+", color_index=0, mode="up")
        overlay_node(pbs_nodes[0], show=f"{fragment + 1}+", color_index=1, mode="down")
        overlay_node(pbs_nodes[1], show=f"{fragment + 1}+", color_index=2)

    # @slides.slide()
    # def autoalloc(slide: Box):
    #     content = slide_header_top(slide, "Automatic allocation")
    #     lst = unordered_list(content.box())
    #     lst.item().text("Automatic submit of PBS/Slurm jobs")
    #     lst.item(show="next+").text("Based on computational demand (submitted tasks)")
    #     lst.item(show="next+").text("To be further improved and analysed")

    # @slides.slide()
    # def autoalloc_diagram(slide: Box):
    #     content = slide_header_top(slide, "Automatic allocation")
    #
    #     hq_box = content.box(y=80)
    #     hq_box.box(width=300).image("images/hq-logo.png")
    #
    #     margin_horizontal = 150
    #     column_height = 300
    #
    #     def label(column: Box, name: str):
    #         return column.box(y=0, p_bottom=20).text(name)
    #
    #     row = content.box(horizontal=True)
    #     task_box = row.box(height=column_height, p_right=margin_horizontal)
    #     task_box_label = label(task_box, "Tasks")
    #     task_size = 40
    #     tasks = task_graph_grid(task_box.box(), size=task_size, rows=1, cols=3,
    #                             task_constructor=create_empty_task_fn(task_size))
    #
    #     pbs_box = row.box(height=column_height, p_right=margin_horizontal)
    #     pbs_box_label = label(pbs_box, "PBS")
    #     queue = SlurmQueue(pbs_box.box(), entries=4, width=160, height=50)
    #
    #     cluster_box = row.box(height=column_height)
    #     node_size = 60
    #     cluster_box_label = label(cluster_box, "Cluster")
    #     nodes = cluster_1(cluster_box.box(), size=node_size)
    #
    #     hq_box.line((
    #         (task_box_label.x("50%"), task_box_label.y(0)),
    #         (task_box_label.x("50%"), hq_box.y("50%")),
    #         (hq_box.x(0), hq_box.y("50%")),
    #     ))
    #     hq_box.line((
    #         (cluster_box_label.x("50%"), cluster_box_label.y(0)),
    #         (cluster_box_label.x("50%"), hq_box.y("50%")),
    #         (hq_box.x("100%"), hq_box.y("50%")),
    #     ))
    #     hq_box.line((
    #         (pbs_box_label.x("50%"), pbs_box_label.y(0)),
    #         (pbs_box_label.x("50%"), hq_box.y("100%")),
    #     ))
    #
    #     def show_task(index: int, show: str):
    #         task_box = tasks[index]
    #         task(task_box.overlay(show=show), x=task_size / 2, y=task_size / 2, size=task_size,
    #              bg_color=get_task_color(index))
    #
    #     def hide_task(index: int, show: str):
    #         task_box = tasks[index]
    #         size = task_size + 10
    #         task_box.overlay(show=show, x=-5, y=-5, width=size, height=size, z_level=2).rect(
    #             bg_color="white")
    #
    #     def show_node(index: int, show: str, job: str, task: Optional[str] = None):
    #         node_box = nodes[index]
    #         node(node_box.overlay(show=show), x=node_size / 2, y=node_size / 2, size=node_size,
    #              color=job, bg_color=task if task is not None else "white",
    #              node_args=dict(stroke_width=4), z_level=2)
    #
    #     def get_job_color(index: int) -> str:
    #         job_color = sns.color_palette()[::-1][index]
    #         return sns_to_elsie_color(job_color)
    #
    #     # Task appears
    #     show_task(0, "2+")
    #     # Backlog is created
    #     entries = queue.set_state([SlurmEntry("job1", "Q"), SlurmEntry("job2", "Q")], show="3+")
    #
    #     arrows = content.overlay(show="4")
    #     offset = 15
    #     arrows.line((
    #         (entries[0].x("100%").add(offset), entries[0].y("50%")),
    #         (entries[0].x("100%").add(offset * 2), entries[0].y("50%")),
    #         (entries[1].x("100%").add(offset * 2), entries[1].y("50%")),
    #         (entries[1].x("100%").add(offset), entries[1].y("50%")),
    #     ))
    #     text = arrows.box(x=entries[0].x("100%").add(offset * 3), y=entries[0].y("100%").add(-12))
    #     text.text("backlog", style=T(size=20))
    #     # arrows.line(())
    #
    #     # First job starts
    #     queue.set_state([SlurmEntry("job1", "R", get_job_color(0)), SlurmEntry("job2", "Q")],
    #                     show="5-7")
    #     show_node(0, show="5", job=get_job_color(0))
    #     show_node(0, show="6+", job=get_job_color(0), task=get_task_color(0))
    #     queue.set_state(
    #         [SlurmEntry("job1", "R", get_job_color(0)), SlurmEntry("job2", "Q"), SlurmEntry("job3", "Q")],
    #         show="7+")
    #
    #     show_task(1, "8+")
    #     queue.set_state(
    #         [SlurmEntry("job1", "R", get_job_color(0)),
    #          SlurmEntry("job2", "R", get_job_color(1)),
    #          SlurmEntry("job3", "Q")],
    #         show="9+")
    #     show_node(1, show="9+", job=get_job_color(1))
    #     show_node(1, show="10+", job=get_job_color(1), task=get_task_color(1))
    #     queue.set_state(
    #         [SlurmEntry("job1", "R", get_job_color(0)),
    #          SlurmEntry("job2", "R", get_job_color(1)),
    #          SlurmEntry("job3", "Q"),
    #          SlurmEntry("job4", "Q")],
    #         show="11+")
    #     show_node(0, show="12+", job=get_job_color(0))
    #     hide_task(0, show="12+")
    #     show_task(2, "13+")
    #     show_node(0, show="14+", job=get_job_color(0), task=get_task_color(2))

    @slides.slide()
    def resources(slide: Box):
        content = slide_header_top(slide, "Challenge: heterogeneous resource management")

        lst = unordered_list(content.box(p_top=80))
        lst.item(show="next+").text("Arbitrary resources")
        lst2 = lst.ul()
        lst2.item().text("GPUs, FPGAs, NICs, …", style="l2")
        lst.item(show="next+").text("Non-fungible resources")
        lst2 = lst.ul()
        lst2.item().text('Resources have identity: "Execute task on GPUs 0 and 3"', style="l2")
        lst.item(show="next+").text("Related resources")
        lst2 = lst.ul()
        lst2.item().text("Task requires 4 cores in the same NUMA node", style="l2")
        lst.item(show="next+").text("Fractional resources")
        lst2 = lst.ul()
        lst2.item().text("Task requires 0.5 of a GPU", style="l2")
        lst.item(show="next+").text("Resource variants")
        lst2 = lst.ul()
        lst2.item().text("Task requires (1 GPU AND 1 CPU) OR 16 CPUs", style="l2")

    @slides.slide()
    def hq_software(slide: Box):
        slide.box(width=500).image("images/hq-logo.png")
        github_link(slide.box(), "github.com/it4innovations/hyperqueue", style=T(size=30))

        slide.box(p_top=100, show="next+").text("Task runtime designed for HPC use-cases")

        row = slide.box(p_top=80, horizontal=True, show="next+")
        margin = 50
        row.box(width=400, p_right=margin).image("images/it4i-logo.png")
        row.box(width=300, p_right=margin).image("images/ligate-logo.png")

        # slide.box(show="next+", p_top=40).text("Team effort @ IT4I")
        # slide.box(show="last+").text("(primary contributors: Ada Böhm & me)", style="l2")

    @slides.slide()
    def hq_architecture(slide: Box):
        content = slide_header_top(slide, "Architecture")
        content.box(width="45%", p_top=40).image("images/hq-architecture.png")

    @slides.slide()
    def hq_solutions(slide: Box):
        content = slide_header_top(slide, "HyperQueue solutions for workflow challenges")
        content.update_style("default", T(size=46))

        lst = unordered_list(content.box(p_top=120))
        lst.item().text("Meta-scheduling")
        lst2 = lst.ul()
        lst2.item().text("Automatic allocation", style="l2")
        lst.item(show="next+").text("Heterogeneous resource scheduling")
        lst.item(show="next+").text("Multi-node tasks")
        lst2 = lst.ul()
        lst2.item().text("Integrated with single node tasks", style="l2")
        lst.item(show="next+").text("Fault-tolerance")
        lst2 = lst.ul()
        lst2.item().text("Worker and server resilience", style="l2")
        lst.item(show="next+").text("I/O streaming")
        lst2 = lst.ul()
        lst2.item().text("Reduces networked filesystem contention", style="l2")
        lst.item(show="next+").text("Several programming interfaces")
        lst2 = lst.ul()
        lst2.item().text("CLI, TOML workflow files, Python API", style="l2")
        lst.item(show="next+").text("Trivial deployment")
        lst2 = lst.ul()
        lst2.item().text("Single binary, no dependencies, no ~emph{sudo} needed", style="l2")

    @slides.slide()
    def hq_scalability(slide: Box):
        content = slide_header_top(slide, "Scalability evaluation")
        content.box(p_top=80).image("images/hq-evaluation-strong-scalability.png")

    @slides.slide()
    def hq_scalability_dask(slide: Box):
        content = slide_header_top(slide, "Scalability vs Dask evaluation")
        content.box(height="80%", p_top=80).image("images/hq-evaluation-scalability-dask.png")

    @slides.slide()
    def hq_overhead(slide: Box):
        content = slide_header_top(slide, "Overhead evaluation")
        content.box(p_top=80).image("images/hq-evaluation-overhead.png")

    @slides.slide()
    def hq_fractional_resources(slide: Box):
        content = slide_header_top(slide, "Fractional resources evaluation")
        content.box().image("images/hq-evaluation-fractional-resources.png")

    @slides.slide()
    def hq_resource_variants(slide: Box):
        content = slide_header_top(slide, "Resource variants evaluation")
        content.box().image("images/hq-evaluation-resource-variants.png")

    @slides.slide()
    def hq_sota_comparison(slide: Box):
        content = slide_header_top(slide, "Comparison of HQ and similar tools")
        content.box(width=1100, p_top=100).image("images/hq-comparison-table.png")

    @slides.slide()
    def hyperqueue_usage(slide: Box):
        content = slide_header_top(slide, "HyperQueue impact")
        content.set_style("l3", style=T(size=28))

        def make_list(slot: Box, show="next+") -> ListBuilder:
            return unordered_list(slot.box(show=show, x=0, y=0))

        def text_with_logo(builder: ListBuilder, text: str, image: str, width=140):
            item = builder.item()
            row = item.box(horizontal=True, height=60)
            row.box(width=width, height="100%").image(image)
            row.box(p_left=15).text(text, style="l3")

        def logo(builder: ListBuilder, image: str, width=140):
            item = builder.item()
            item.box(width=width).image(image)

        def iterate_grid(box: Box, width: int, height: int, rows: int, cols: int) -> Iterable[Box]:
            box = box.box(width=width, height=height)

            box_width = width / cols
            box_height = height / rows

            index = 0
            for row in range(rows):
                for col in range(cols):
                    x_offset = 0 if col == 0 else 25
                    x = col * box_width + x_offset
                    if index == 2:
                        x = "[35%]"
                    item = box.box(width=box_width, height=box_height, x=x, y=row * box_height)
                    yield item
                    index += 1

        for (index, slot) in enumerate(
                iterate_grid(content.box(x=200, y=150), width=1400, height=800, rows=2, cols=2)):
            if index == 0:
                lst = make_list(slot, show="1+")
                lst.item().text("EU projects")
                lst2 = lst.ul()
                text_with_logo(lst2, "Complex workflows, Python API",
                               "images/ligate-logo.png")
                text_with_logo(lst2, "Heterogeneous resources",
                               "images/everest-logo.png")
                text_with_logo(lst2, "Multi-node tasks",
                               "images/across-logo.jpg")
                text_with_logo(lst2, "Server resilience, data transfers",
                               "images/max-logo.png")
            elif index == 1:
                lst = make_list(slot)
                lst.item().text("HPC centers")
                lst2 = lst.ul()
                logo(lst2, "images/it4i-logo.png", width=300)
                logo(lst2, "images/lumi-logo.png")
                logo(lst2, "images/cineca-logo.png")
                logo(lst2, "images/csc-logo.svg")
            elif index == 2:
                lst = make_list(slot)
                lst.item().text("Integration in other tools")

                row = slot.box(horizontal=True, x=120)
                lst = unordered_list(row.box())
                logo(lst, "images/nextflow-logo.png")
                logo(lst, "images/aiida-logo.png")
                logo(lst, "images/streamflow-logo.png")

                lst = unordered_list(row.box(p_left=100))
                logo(lst, "images/um-bridge-logo.png", width=80)
                logo(lst, "images/heappe-logo.png", width=80)
                lst.item().text("ERT")

    @slides.slide()
    def hyperqueue_research_cern(slide: Box):
        slide.set_style("small", T(size=30))

        content = slide_header_top(slide, "HyperQueue impact")

        col = content.box(x="[70%]", p_top=140)
        col.box().text("ATLAS experiment (CERN)")
        col.box(p_top=10).text("ARC-CE+HyperQueue based submission system of\nATLAS jobs for the Karolina HPC", style="small")
        content.box(x="[10%]", y="[50%]", width=350).image("images/cern-hq-poster.png")

        col.box(width=550, show="next+", p_top=20).image("images/cern-hq-efficiency.png")

    @slides.slide()
    def hyperqueue_research_ligate(slide: Box):
        slide.set_style("small", T(size=40))

        content = slide_header_top(slide, "HyperQueue impact")
        content.box(p_top=120).text(
            "LIGATE Pose selector workflow",
        )
        lst = unordered_list(content.box(p_top=20))
        lst.item(show="next+").text("6M+ MD simulations on 4k+ ligands", "small")
        lst.item().text("240k GPU hours on LUMI-G cluster", "small")
        lst.item().text("2M CPU hours on MeluXina cluster", "small")

        quotation(content.box(p_top=40, show="next+"), """...making both workflows some of the largest
molecular dynamics campaigns ever performed...""", "LIGATE Deliverable D7.1 (lessons learned)")

    @slides.slide()
    def hq_outcome(slide: Box):
        content = slide_header_top(slide, "Outcome")

        lst = unordered_list(content.box(p_top=100))
        lst.item(show="next+").text("Integrated solution for workflows on HPC")
        lst.item(show="next+").text("Ergonomics")
        lst2 = lst.ul()
        lst2.item().text("Meta-scheduling", style="l2")
        lst2.item().text("Fine-grained heterogeneous resource management", style="l2")
        lst2.item().text("Multi-node tasks", style="l2")
        lst2.item().text("Trivial deployment", style="l2")
        lst.item(show="next+").text("Efficiency")
        lst2 = lst.ul()
        lst2.item().text("Low overhead per task", style="l2")
        lst2.item().text("Millions of tasks, hundreds of nodes", style="l2")
        lst.item(show="next+").text("Open source")
        lst2 = lst.ul()
        github_link(lst2.item(), "github.com/it4innovations/hyperqueue", style="l2")
