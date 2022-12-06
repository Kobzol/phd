import dataclasses
from typing import Iterable, List, Optional, Union

import seaborn as sns
from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.ext.list import ListBuilder

from tasks import cluster_1, get_task_color, half_node, node, sns_to_elsie_color, task, \
    task_graph_2, task_graph_grid
from utils import bash, code, slide_header_top


@dataclasses.dataclass
class PbsEntry:
    label: str = ""
    state: str = ""
    color: Optional[str] = None


class PbsQueue:
    def __init__(self, box: Box, entries: int, width=200, height=60):
        self.box = box.box(width=width, height=height * entries)
        self.width = width
        self.height = height

        self.set_state([PbsEntry() for _ in range(entries)], show="1+")

    def set_state(self, entries: List[PbsEntry], show: str) -> List[Box]:
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
    def hyperqueue_intro(slide: Box):
        slide.box(width=400).image("images/hq-logo.png")
        slide.box().text("Task runtime designed for HPC")

        slide.box(show="next+", p_top=40).text("Team effort @ IT4I")
        slide.box(show="last+").text("(primary contributors: Ada Böhm & me)", style="l2")

    @slides.slide()
    def hq_architecture(slide: Box):
        content = slide_header_top(slide, "Architecture")
        content.box(width="70%").image("images/hq-architecture.png")

    @slides.slide()
    def hq_usage_bash(slide: Box):
        content = slide_header_top(slide, "Command-line interface")

        width = 900
        margin = 20
        x = 60
        content.box(p_bottom=margin / 2).text("Start server")

        style = TextStyle(size=26)
        bash(content.box(width=width, x=x, p_bottom=margin), "(login1) $ hq server start",
             text_style=style)

        box = content.sbox(show="next+")
        box.box(p_bottom=margin / 2, ).text("Submit tasks")
        bash(box.box(width=width, x=x, p_bottom=margin),
             "(login1) $ hq submit -- ./my-program --foo=bar",
             text_style=style)

        box = content.sbox(show="next+")
        box.box(p_bottom=margin / 2, ).text("Provide computational resources")
        bash(box.box(width=width, x=x),
             "(login1) $ hq alloc add pbs --time-limit 1h -- -qqexp",
             text_style=style)
        box.box(p_bottom=margin / 2, show="next+").text("or")
        bash(box.box(width=width, x=x, show="last+"), "(node1)  $ hq worker start",
             text_style=style)

    @slides.slide()
    def hq_usage_python(slide: Box):
        content = slide_header_top(slide, "Python API")

        width = 800
        code(content.box(width=width, show="last+"), """def preprocess(path):
    # preprocess data

path = "/tmp/foo"

job = Job()
t1 = job.function(preprocess, args=(path, ))
job.program(["simulate", "--path", path], deps=[t1])
client.submit(job)""", width=width, language="python")

    @slides.slide()
    def challenge_pbs(slide: Box):
        content = slide_header_top(slide, "Challenge: PBS/Slurm")
        content.box(p_bottom=60).text("Disentangle computation & resource provisioning")

        width = 800
        row = content.box(horizontal=True, p_bottom=40, width=width, show="next+")
        row.box(x=0).text("PBS")

        pbs_start = 3
        margin_left = 300
        node_size = 40
        task_size = 40

        def pbs_task(box, x, y, name, size, row, col):
            index = row * 3 + col
            bg_color = get_task_color(index)
            if row == 0:
                show = f"{pbs_start}+"
            elif col < 2:
                show = f"{pbs_start + 1}+"
            else:
                show = f"{pbs_start + 2}+"
            return task(box=box, x=x, y=y, name=None, size=size, bg_color=bg_color, show=show)

        task_graph_2(row.box(p_left=margin_left), size=task_size, task_constructor=pbs_task)

        def pbs_cluster(box, x, y, size, diagonal, index):
            index += {
                0: 0,
                1: 3,
                2: 5
            }[diagonal]
            if diagonal == 0:
                show = f"{pbs_start}+"
            elif diagonal == 1:
                show = f"{pbs_start + 1}+"
            else:
                show = f"{pbs_start + 2}+"
            return node(box, x=x, y=y, size=size, bg_color=get_task_color(index), show=show,
                        node_args=dict(stroke_width=4))

        box = row.box(p_left=100)
        cluster_1(box.box(), size=node_size)
        cluster_1(box.overlay(), size=node_size, node_constructor=pbs_cluster)

        row = content.box(horizontal=True, width=width, show="next+")
        row.box(x=0).text("PBS + HyperQueue")

        hq_start = box.current_fragment()

        def hq_show(count=0, duration: Optional[int] = None) -> str:
            if duration is None:
                return f"{hq_start + count}+"
            else:
                return f"{hq_start + count}-{hq_start + count + duration}"

        tasks = task_graph_2(row.box(p_left=margin_left), size=task_size,
                             task_constructor=create_empty_task_fn(task_size))

        nodes = cluster_1(row.box(p_left=100), size=node_size)

        def overlay_node(node_index: int, timestep: int,
                         color_index: Optional[Union[int, str]] = None,
                         mode="full"):
            node_box = nodes[node_index]
            show = hq_show(timestep)
            box = node_box.overlay()
            modes = {
                "full": node,
                "up": lambda **args: half_node(mode="up", **args),
                "down": lambda **args: half_node(mode="down", **args)
            }

            stroke_width = 4 if mode == "full" else 2
            modes[mode](box=box, x=node_size / 2, y=node_size / 2, size=node_size,
                        bg_color=get_task_color(color_index),
                        show=show, node_args=dict(stroke_width=stroke_width))

        def overlay_task(task_indices: List[int], timestep: int, color_index: int):
            for task_index in task_indices:
                task_box = tasks[task_index]
                show = hq_show(timestep)
                box = task_box.overlay()
                task(box=box, x=task_size / 2, y=task_size / 2, size=node_size,
                     bg_color=get_task_color(color_index),
                     show=show)

        overlay_task([0], 1, 0)
        overlay_task([1], 1, 1)
        overlay_node(0, 2, "white")
        overlay_node(0, 3, 0, mode="up")
        overlay_node(0, 3, 1, mode="down")
        overlay_task([2], 4, 2)
        overlay_node(3, 4, 2)
        overlay_task([3], 5, 3)
        overlay_node(0, 5, 3, mode="down")
        overlay_task([4], 6, 4)
        overlay_task([5], 6, 5)
        overlay_node(3, 6, 4, mode="up")
        overlay_node(3, 6, 5, mode="down")

    @slides.slide()
    def autoalloc(slide: Box):
        content = slide_header_top(slide, "Automatic allocation")
        lst = unordered_list(content.box())
        lst.item().text("Automatic submit of PBS/Slurm jobs")
        lst.item(show="next+").text("Based on computational demand (submitted tasks)")
        lst.item(show="next+").text("To be further improved and analysed")

    @slides.slide()
    def autoalloc_diagram(slide: Box):
        content = slide_header_top(slide, "Automatic allocation")

        hq_box = content.box(y=80)
        hq_text = hq_box.box(width=300).image("images/hq-logo.png")

        margin_horizontal = 150
        column_height = 300

        def label(column: Box, name: str):
            return column.box(y=0, p_bottom=20).text(name)

        row = content.box(horizontal=True)
        task_box = row.box(height=column_height, p_right=margin_horizontal)
        task_box_label = label(task_box, "Tasks")
        task_size = 40
        tasks = task_graph_grid(task_box.box(), size=task_size, rows=1, cols=3,
                                task_constructor=create_empty_task_fn(task_size))

        pbs_box = row.box(height=column_height, p_right=margin_horizontal)
        pbs_box_label = label(pbs_box, "PBS")
        queue = PbsQueue(pbs_box.box(), entries=4, width=160, height=50)

        cluster_box = row.box(height=column_height)
        node_size = 60
        cluster_box_label = label(cluster_box, "Cluster")
        nodes = cluster_1(cluster_box.box(), size=node_size)

        hq_box.line((
            (task_box_label.x("50%"), task_box_label.y(0)),
            (task_box_label.x("50%"), hq_box.y("50%")),
            (hq_box.x(0), hq_box.y("50%")),
        ))
        hq_box.line((
            (cluster_box_label.x("50%"), cluster_box_label.y(0)),
            (cluster_box_label.x("50%"), hq_box.y("50%")),
            (hq_box.x("100%"), hq_box.y("50%")),
        ))
        hq_box.line((
            (pbs_box_label.x("50%"), pbs_box_label.y(0)),
            (pbs_box_label.x("50%"), hq_box.y("100%")),
        ))

        def show_task(index: int, show: str):
            task_box = tasks[index]
            task(task_box.overlay(show=show), x=task_size / 2, y=task_size / 2, size=task_size,
                 bg_color=get_task_color(index))

        def hide_task(index: int, show: str):
            task_box = tasks[index]
            size = task_size + 10
            task_box.overlay(show=show, x=-5, y=-5, width=size, height=size, z_level=2).rect(
                bg_color="white")

        def show_node(index: int, show: str, job: str, task: Optional[str] = None):
            node_box = nodes[index]
            node(node_box.overlay(show=show), x=node_size / 2, y=node_size / 2, size=node_size,
                 color=job, bg_color=task if task is not None else "white",
                 node_args=dict(stroke_width=4), z_level=2)

        def get_job_color(index: int) -> str:
            job_color = sns.color_palette()[::-1][index]
            return sns_to_elsie_color(job_color)

        # Task appears
        show_task(0, "2+")
        # Backlog is created
        entries = queue.set_state([PbsEntry("job1", "Q"), PbsEntry("job2", "Q")], show="3+")

        arrows = content.overlay(show="4")
        offset = 15
        arrows.line((
            (entries[0].x("100%").add(offset), entries[0].y("50%")),
            (entries[0].x("100%").add(offset * 2), entries[0].y("50%")),
            (entries[1].x("100%").add(offset * 2), entries[1].y("50%")),
            (entries[1].x("100%").add(offset), entries[1].y("50%")),
        ))
        text = arrows.box(x=entries[0].x("100%").add(offset * 3), y=entries[0].y("100%").add(-12))
        text.text("backlog", style=TextStyle(size=20))
        # arrows.line(())

        # First job starts
        queue.set_state([PbsEntry("job1", "R", get_job_color(0)), PbsEntry("job2", "Q")],
                        show="5-7")
        show_node(0, show="5", job=get_job_color(0))
        show_node(0, show="6+", job=get_job_color(0), task=get_task_color(0))
        queue.set_state(
            [PbsEntry("job1", "R", get_job_color(0)), PbsEntry("job2", "Q"), PbsEntry("job3", "Q")],
            show="7+")

        show_task(1, "8+")
        queue.set_state(
            [PbsEntry("job1", "R", get_job_color(0)),
             PbsEntry("job2", "R", get_job_color(1)),
             PbsEntry("job3", "Q")],
            show="9+")
        show_node(1, show="9+", job=get_job_color(1))
        show_node(1, show="10+", job=get_job_color(1), task=get_task_color(1))
        queue.set_state(
            [PbsEntry("job1", "R", get_job_color(0)),
             PbsEntry("job2", "R", get_job_color(1)),
             PbsEntry("job3", "Q"),
             PbsEntry("job4", "Q")],
            show="11+")
        show_node(0, show="12+", job=get_job_color(0))
        hide_task(0, show="12+")
        show_task(2, "13+")
        show_node(0, show="14+", job=get_job_color(0), task=get_task_color(2))

    @slides.slide()
    def resources(slide: Box):
        content = slide_header_top(slide, "Challenge: fine-grained resources")
        lst = unordered_list(content.box())
        lst.item().text("Arbitrary resources per task and worker")
        lst.item(show="next+").text("Resource-aware scheduler")
        lst.item(show="next+").text("NUMA support")

        width = 1000
        bash(content.box(width=width, p_top=20, show="next+"),
             "$ hq worker start --resource gpus=range(1-3)")
        bash(content.box(width=width, p_top=40, show="next+"),
             "$ hq submit --cpus=4 --resources gpus=2 ...")

        # TODO: diagram

    @slides.slide()
    def multinode_tasks(slide: Box):
        content = slide_header_top(slide, "Challenge: multi-node tasks")
        lst = unordered_list(content.box())
        lst.item().text("Initial support for multi-node tasks")

        bash(content.box(width=600, p_top=40, show="next+"), "$ hq submit --nodes=4 ...")

    # @slides.slide()
    # def hq_ergonomics(slide: Box):
    #     content = slide_header_top(slide, "HQ: ergonomics")
    #     lst = unordered_list(content.box())
    #     lst.item().text("Computation definition/provisioning disentangled")
    #     lst.item(show="next+").text("No manual PBS/Slurm interaction needed")
    #     lst2 = lst.ul()
    #     lst2.item().text("Automatic PBS/Slurm allocation", style="l2")
    #     lst.item(show="next+").text("Fine-grained generic resource requirements")
    #     lst2 = lst.ul()
    #     lst2.item().text("Core count, memory usage, GPU count, FPGA count, …", style="l2")
    #     lst.item(show="next+").text("Trivial deployment")
    #     lst2 = lst.ul()
    #     lst2.item().text("Single binary, no dependencies, no ~tt{sudo}", style="l2")

    @slides.slide()
    def hq_efficiency(slide: Box):
        content = slide_header_top(slide, "Challenge: efficiency")
        lst = unordered_list(content.box())
        lst.item().text("Low overhead per task (~0.1ms)", escape_char="|")
        lst.item(show="next+").text("I/O streaming: ~tt{stdout/stderr} over network")

    @slides.slide()
    def hyperqueue_usage(slide: Box):
        content = slide_header_top(slide, "HyperQueue in the wild")

        def make_list(slot: Box, show="next+") -> ListBuilder:
            return unordered_list(slot.box(show=show, x=0, y=0))

        def item_with_logo(builder: ListBuilder, text: str, image: str, width=120):
            item = builder.item()
            row = item.box(horizontal=True)
            row.box(width=230).text(text, style="l2")
            row.box(width=width).image(image)

        for (index, slot) in enumerate(
                iterate_grid(content.box(y=50), width=900, height=400, rows=2, cols=2)):
            if index == 0:
                lst = make_list(slot, show="1+")
                lst.item().text("H2020 EU projects")
                lst2 = lst.ul()
                item_with_logo(lst2, "LIGATE", "images/ligate-logo.png")
                item_with_logo(lst2, "EVEREST", "images/everest-logo.png")
                item_with_logo(lst2, "ACROSS", "images/across-logo.jpg")
            elif index == 1:
                lst = make_list(slot)
                lst.item().text("HPC centers")
                lst2 = lst.ul()
                item_with_logo(lst2, "IT4Innovations", "images/it4i-logo.png", width=200)
                item_with_logo(lst2, "LUMI", "images/lumi-logo.png")
            elif index == 2:
                lst = make_list(slot)
                lst.item().text("Integrations")
                lst2 = lst.ul()
                item_with_logo(lst2, "NextFlow", "images/nextflow-logo.png")
                item_with_logo(lst2, "Aiida", "images/aiida-logo.png")
                item_with_logo(lst2, "ERT", "images/across-logo.jpg")
            else:
                slot.set_style("small", TextStyle(size=16))
                lst = make_list(slot)
                lst.item().text("Research")
                lst2 = lst.ul()
                lst2.item().text(
                    "ATLAS experiment (CERN)\n~small{ARC-CE+HyperQueue based submission system of\nATLAS jobs for the Karolina HPC}",
                    style=slide.get_style("l2").compose(TextStyle(line_spacing=0.8))
                )
                lst2.item(p_top=20).text("Supercomputing'21 poster", style="l2")
                lst2.item(width=200, height=250, label="").image("images/hq-poster.png")


def iterate_grid(box: Box, width: int, height: int, rows: int, cols: int) -> Iterable[Box]:
    box = box.box(width=width, height=height)

    box_width = width / cols
    box_height = height / rows

    for row in range(rows):
        for col in range(cols):
            item = box.box(width=box_width, height=box_height, x=col * box_width,
                           y=row * box_height)
            yield item
