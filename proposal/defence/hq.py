from typing import Iterable, List, Optional, Union

import seaborn as sns
from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.ext.list import ListBuilder

from tasks import cluster_1, half_node, node, task, task_graph_2
from utils import bash, code, slide_header_top


def hyperqueue(slides: Slides):
    @slides.slide()
    def hyperqueue(slide: Box):
        slide.box(width=400).image("images/hq-logo.png")
        slide.box().text("Task runtime designed for HPC")

        slide.box(show="next+", p_top=40).text("Team effort @ IT4I")
        slide.box(show="last+").text("(primary contributors: Ada Böhm & me)", style="l2")

    @slides.slide()
    def key_idea(slide: Box):
        content = slide_header_top(slide, "Key idea")
        content.box(p_bottom=60).text("Disentangle computation & resource provisioning")

        width = 800
        row = content.box(horizontal=True, p_bottom=40, width=width, show="next+")
        row.box(x=0, p_right=50).text("PBS")

        palette = sns.color_palette()

        pbs_start = 3
        margin_right = 100
        node_size = 40
        task_size = 40

        def get_color(index: Union[int, str]):
            if isinstance(index, str):
                return index
            color = tuple(int(v * 255) for v in palette[index])
            return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()

        def pbs_task(box, x, y, name, size, row, col):
            index = row * 3 + col
            bg_color = get_color(index)
            if row == 0:
                show = f"{pbs_start}+"
            elif col < 2:
                show = f"{pbs_start + 1}+"
            else:
                show = f"{pbs_start + 2}+"
            return task(box=box, x=x, y=y, name=None, size=size, bg_color=bg_color, show=show)

        box = row.box(p_right=margin_right)
        task_graph_2(box, size=task_size, task_constructor=pbs_task)

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
            return node(box, x=x, y=y, size=size, bg_color=get_color(index), show=show,
                        node_args=dict(stroke_width=4))

        box = row.box()
        cluster_1(box.box(), size=node_size)
        cluster_1(box.overlay(), size=node_size, node_constructor=pbs_cluster)

        row = content.box(horizontal=True, width=width, show="next+")
        row.box(x=0, p_right=50).text("HyperQueue")

        hq_start = box.current_fragment()

        def hq_show(count=0, duration: Optional[int] = None) -> str:
            if duration is None:
                return f"{hq_start + count}+"
            else:
                return f"{hq_start + count}-{hq_start + count + duration}"

        def hq_task(box, x, y, name, size, row, col):
            return box.box(x=x, y=y, width=task_size, height=task_size)

        tasks = task_graph_2(row.box(p_right=margin_right), size=task_size,
                             task_constructor=hq_task)

        nodes = cluster_1(row.box(), size=node_size)

        def overlay_node(node_index: int, timestep: int, color_index: Optional[int] = None,
                         mode="full"):
            node_box = nodes[node_index]
            show = hq_show(timestep)
            box = node_box.overlay()
            modes = {
                "full": node,
                "up": lambda **args: half_node(up=True, **args),
                "down": lambda **args: half_node(up=False, **args)
            }

            stroke_width = 4 if mode == "full" else 2
            modes[mode](box=box, x=node_size / 2, y=node_size / 2, size=node_size,
                        bg_color=get_color(color_index),
                        show=show, node_args=dict(stroke_width=stroke_width))

        def overlay_task(task_indices: List[int], timestep: int, color_index: int):
            for task_index in task_indices:
                task_box = tasks[task_index]
                show = hq_show(timestep)
                box = task_box.overlay()
                task(box=box, x=task_size / 2, y=task_size / 2, size=node_size,
                     bg_color=get_color(color_index),
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
    def hq_architecture(slide: Box):
        content = slide_header_top(slide, "Architecture")
        content.box(width="70%").image("images/hq-architecture.png")

    @slides.slide()
    def hq_usage(slide: Box):
        content = slide_header_top(slide, "Usage example")

        width = 600
        content.box(p_bottom=10).text("Bash")
        bash(content.box(width=width), """$ hq server start

$ hq submit          \\
  --array 1-100      \\
  --resource cpus=2  \\
  -- ./my-program --param=10
""", text_style=TextStyle(size=26))

        content.box(p_top=40, p_bottom=10, show="next+").text("Python API")
        code(content.box(width=width, show="last+"), """def preprocess(path):
    # preprocess data

path = "/tmp/foo"

job = Job()
t1 = job.function(preprocess, args=(path, ))
job.program(["simulate", "--path", path], deps=[t1])
client.submit(job)""", width=width, language="python")

    @slides.slide()
    def hq_ergonomics(slide: Box):
        content = slide_header_top(slide, "HQ: ergonomics")
        lst = unordered_list(content.box())
        lst.item().text("Computation definition/provisioning disentangled")
        lst.item(show="next+").text("No manual PBS/Slurm interaction needed")
        lst2 = lst.ul()
        lst2.item().text("Automatic PBS/Slurm allocation", style="l2")
        lst.item(show="next+").text("Fine-grained generic resource requirements")
        lst2 = lst.ul()
        lst2.item().text("Core count, memory usage, GPU count, FPGA count, …", style="l2")
        lst.item(show="next+").text("Trivial deployment")
        lst2 = lst.ul()
        lst2.item().text("Single binary, no dependencies, no ~tt{sudo}", style="l2")

    @slides.slide()
    def hq_autoalloc(slide: Box):
        content = slide_header_top(slide, "Automatic allocation")
        lst = unordered_list(content.box())
        lst.item().text("Background process, spawns PBS/Slurm allocations")
        lst.item(show="next+").text("Based on computational demand (submitted tasks)")
        lst.item(show="next+").text("Users define queue parameters")
        # TODO: diagram

    @slides.slide()
    def hq_efficiency(slide: Box):
        content = slide_header_top(slide, "HQ: efficiency")
        lst = unordered_list(content.box())
        lst.item().text("Low overhead per task (~0.1ms)", escape_char="|")
        lst.item(show="next+").text("I/O overhead reduction")
        lst2 = lst.ul()
        lst2.item().text("I/O streaming: ~tt{stdout/stderr} over network")

    @slides.slide()
    def hyperqueue_usage(slide: Box):
        content = slide_header_top(slide, "HyperQueue usage")

        def make_list(slot: Box, show="next+") -> ListBuilder:
            return unordered_list(slot.box(show=show, x=0, y=0))

        def item_with_logo(builder: ListBuilder, text: str, image: str):
            item = builder.item()
            row = item.box(horizontal=True)
            row.box(p_right=20).text(text, style="l2")
            row.box(width=80).image(image)

        for (index, slot) in enumerate(
                iterate_grid(content, width=900, height=400, rows=2, cols=2)):
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
                item_with_logo(lst2, "IT4Innovations", "images/it4i-logo.png")
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
                    style="l2"
                )


def iterate_grid(box: Box, width: int, height: int, rows: int, cols: int) -> Iterable[Box]:
    box = box.box(width=width, height=height)

    box_width = width / cols
    box_height = height / rows

    for row in range(rows):
        for col in range(cols):
            item = box.box(width=box_width, height=box_height, x=col * box_width,
                           y=row * box_height)
            yield item
