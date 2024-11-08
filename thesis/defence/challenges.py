import random
from typing import List, Optional

from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from tasks import cluster_1, get_task_color, node, task, task_graph_1
from utils import slide_header_top


BLUE = "#608BC1"
RED = "#FA4032"
GREEN = "#B1D690"
ORANGE = "#FF9D3D"


def header(slide: Box, text: str, ok: Optional[bool] = None, step: Optional[str] = None):
    header = slide.box(horizontal=True, height=120, y=50, show=step)
    header.box(p_right=40).text(text, T(size=60))
    if ok is not None:
        img = "checkmark" if ok else "crossmark"
        header.box(width=50, y=40).image(f"images/{img}.png")


def challenges(slides: Slides):
    @slides.slide()
    def allocation_manager(slide: Box):
        content = slide_header_top(slide, "Allocation manager")

        row = content.box(horizontal=True)
        task_graph_1(row, size=75)

        row.box(p_left=50)
        row.box(width=100).line(
            [(0, "50%"), ("100%", "50%")],
            stroke_width=8,
            end_arrow=Arrow(size=20)
        )
        row.box(p_right=50)
        # TODO: better graphics
        manager = row.box(p_right=100, show="next+")
        manager.rect(color="red", stroke_width=10, stroke_dasharray="16")
        manager.box(padding=50).text("""PBS
Slurm""")

        cluster_box = row.box()
        cluster_1(cluster_box, size=75)

    @slides.slide()
    def large_tasks(slide: Box):
        header(slide, text="A few large tasks", ok=True)

        cols = slide.box(horizontal=True)
        left = cols.box(y=0, width=100)

        tasks = [(0, GREEN), (150, RED), (300, BLUE)]
        for (y, color) in tasks:
            task(left, y=y, bg_color=color)

        right = cols.box(p_left=200)
        cluster_box = right.box()
        cluster_1(cluster_box.fbox(show=1), size=100)

        index = 0

        def get_color():
            nonlocal index
            color = tasks[index][1]
            index = (index + 1) % len(tasks)
            return color

        def filled_node(box, x, y, size, diagonal, index):
            box = node(box, x=x, y=y, size=size)
            if index == 0:
                task(box.box(), size=60, bg_color=get_color())
            return box

        cluster_1(cluster_box.overlay(show=2), size=100, node_constructor=filled_node)

    task_rows = 8
    task_cols = 16
    task_dim = 45

    def render_tasks(parent: Box) -> List[Box]:
        tasks = []

        horizontal_padding = 10
        vertical_padding = 30
        for row in range(task_rows):
            for col in range(task_cols):
                row_coord = row * (task_dim + vertical_padding)
                col_coord = col * (task_dim + horizontal_padding)

                t = task(parent, x=col_coord, y=row_coord, size=task_dim)
                tasks.append(t)
        return tasks

    @slides.slide()
    def many_tasks_overhead(slide: Box):
        header(slide, "Many tasks", ok=False)

        cols = slide.box(x=100, y=220, horizontal=True)
        left = cols.box(width=1000, y=0)
        render_tasks(left)

        cols.update_style("default", T(size=30))
        right = cols.box(horizontal=True, y=0, show="next+")
        submits = right.box()
        for _ in range(15):
            submits.box().text("sbatch script.sh")
        submits.box().text("...")
        submits.box(width=300, x="[50%]", y="[50%]", show="next+").image("images/prohibited.svg")

    @slides.slide()
    def heterogeneous_tasks(slide: Box):
        header(slide, "Heterogeneous tasks", ok=False, step="1")
        header(slide, "Task dependencies", ok=False, step="2")

        cols = slide.box(x=100, y=220, horizontal=True)
        left = cols.box(width=1000, y=0)
        tasks = render_tasks(left)

        colours = [RED, GREEN, BLUE, ORANGE]
        random.seed(42)
        for (index, task_box) in enumerate(tasks):
            task_box = task(task_box.overlay(), x=task_dim / 2, y=task_dim / 2, size=task_dim, bg_color=random.choice(colours))

            row = index // task_cols
            col = index % task_cols
            if row == task_rows - 1:
                continue

            candidates = [col -1] if col != 0 else []
            candidates.append(col)
            if col != task_cols - 1:
                candidates.append(col + 1)
            random.shuffle(candidates)
            targets = [c for c in candidates if random.random() < 0.5]
            for target_col in targets:
                offset = 0
                if target_col < col:
                    offset = 10
                elif target_col > col:
                    offset = -10
                target_index = (row + 1) * task_cols + target_col
                target = tasks[target_index]
                slide.box(show="2+", z_level=-1).line((
                    (task_box.x("50%"), task_box.y("50%")),
                    (target.x("50%").add(offset), target.y("0%"))
                ), stroke_width=3, end_arrow=Arrow())

    @slides.slide()
    def cluster_heterogeneity(slide: Box):
        content = slide_header_top(slide, "Heterogeneous clusters")
        line_box = content.overlay(show="2+")

        nodes = cluster_1(content.box(x="[10%]", y="[50%]"), size=60)
        node = nodes[5]
        line_box.line((
            (node.x("25%"), node.y(0)),
            (660, 300)
        ), stroke_width=2, stroke_dasharray="4")
        line_box.line((
            (node.x("25%"), node.y("100%")),
            (662, 676)
        ), stroke_width=2, stroke_dasharray="4")

        content.box(p_top=60, width="50%").image("images/heterogeneous-node.svg", show_begin=2)

    @slides.slide()
    def multinode_tasks(slide: Box):
        content = slide_header_top(slide, "Multi-node tasks")

        box = content.box(horizontal=True)

        task_size = 60
        tasks = task_graph_1(box=box.box(p_right=100), size=task_size, with_names=False)
        task(box=tasks[0].overlay(), x=task_size / 2, y=task_size / 2, size=task_size,
             bg_color=get_task_color(0))

        node_size = 60
        nodes = cluster_1(box.box(), size=node_size)
        for node_box in nodes[:2]:
            node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                 bg_color=get_task_color(0))

        lst = unordered_list(content.box(p_top=50))
        lst.item(show="next+").text("MPI application within a task")
        lst.item(show="next+").text("Complicates scheduling and data transfers")

    @slides.slide()
    def other_challenges(slide: Box):
        content = slide_header_top(slide, "Other workflow challenges on HPC")

        lst = unordered_list(content.box())
        lst.item().text("Scalability")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Millions of tasks, hundreds of nodes", style="l2")
        lst2.item(show="next+").text("Communication bottleneck", style="l2")
        lst.item(show="next+").text("Fault tolerance")
        lst.item(show="next+").text("Iterative computation")
