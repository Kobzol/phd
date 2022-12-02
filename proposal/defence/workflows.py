from typing import Optional, Tuple, Union

from elsie import Arrow, Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def task(box: Box, x: int, y: int, size=100, name: Optional[str] = None) -> Box:
    box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, z_level=2)
    box.rect(color="black", bg_color="white", stroke_width=4, rx=100, ry=100)
    if name is not None:
        box.text(name)
    return box


def draw_node(box: Box, color="black"):
    box.polygon([
        (box.x("25%"), box.y(0)),
        (box.x("75%"), box.y(0)),
        (box.x("100%"), box.y("50%")),
        (box.x("75%"), box.y("100%")),
        (box.x("25%"), box.y("100%")),
        (box.x(0), box.y("50%")),
    ], color=color)


def node(box: Box, x: int, y: int, size=30, color="black"):
    node_box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size)
    draw_node(node_box, color=color)


def task_top(box: Box) -> Tuple[int, int]:
    return (box.x("50%"), box.y(-5))


def task_bottom(box: Box) -> Tuple[int, int]:
    return (box.x("50%"), box.y("100%"))


def task_point(box: Box, x: Union[int, str], y: Union[int, str]) -> Tuple[int, int]:
    return (box.x(x), box.y(y))


BoxOrPos = Union[Box, Tuple[int, int]]


def edge(box: Box, start: BoxOrPos, end: BoxOrPos, dep=True):
    arrow = Arrow(size=16, stroke_width=5)

    def normalize(pos: BoxOrPos) -> Tuple[int, int]:
        if isinstance(pos, Box):
            return (pos.x("50%"), pos.y("50%"))
        return pos

    box.line(
        points=(normalize(start), normalize(end)),
        end_arrow=arrow,
        color="black",
        stroke_width=5,
        stroke_dasharray=4 if not dep else None
    )


def workflows(slides: Slides):
    @slides.slide()
    def workflows_definition(slide: Box):
        content = slide_header_top(slide, "Task-based workflows")

        lst = unordered_list(content.box())
        lst.item(label="=").text("pipelines, workflows, task graphs, …")
        lst.item(show="next+").text("Popular programming model")

    task_start_center = 500

    @slides.slide()
    def task_definition(slide: Box):
        content = slide_header_top(slide, "Task")

        task(content, task_start_center, 100)

        lst = unordered_list(content.box())
        lst.item().text("Unit of computation")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Fine-grained (function)", style="l2")
        lst2.item(show="next+").text("Coarse-grained (executable binary)", style="l2")
        lst.item(show="next+").text("Execution template (executable repeatedly)")
        lst.item(show="next+").text("Atomic")

    @slides.slide()
    def task_inputs(slide: Box):
        content = slide_header_top(slide, "Task inputs")

        t1 = task(content, task_start_center, 100)
        edge(content, (task_start_center, 0), task_top(t1), dep=False)

        lst = unordered_list(content.box())
        lst.item(show="next+").text("Function arguments")
        lst.item(show="next+").text("CLI arguments")
        lst.item(show="next+").text("Environment variables")

    @slides.slide()
    def task_outputs(slide: Box):
        content = slide_header_top(slide, "Task outputs")

        t1 = task(content, task_start_center, 100)
        edge(content, task_bottom(t1), (task_start_center, 200), dep=False)

        lst = unordered_list(content.box())
        lst.item(show="next+").text("Return value")
        lst.item(show="next+").text("Files on disk")

    @slides.slide()
    def task_dependencies(slide: Box):
        content = slide_header_top(slide, "Task dependencies")

        t1 = task(content, task_start_center, 100, name="t1")
        t2 = task(content, task_start_center, 250, name="t2")
        edge(content, task_bottom(t1), task_top(t2))

        lst = unordered_list(content.box())
        lst.item(show="next+").text("~tt{t2} cannot start before ~tt{t1} completes")

    @slides.slide()
    def task_graphs(slide: Box):
        content = slide_header_top(slide, "Task graphs (workflows)")

        t1 = task(content, task_start_center - 150, 100, name="t1")
        t2 = task(content, task_start_center + 150, 100, name="t2")
        t3 = task(content, task_start_center, 300, name="t3")
        t4 = task(content, task_start_center - 150, 300, name="t4")
        edge(content, task_point(t1, "50%", "50%"), task_point(t3, "25%", 0))
        edge(content, task_point(t2, "50%", "50%"), task_point(t3, "75%", 0))
        edge(content, task_bottom(t1), task_top(t4))

        lst = unordered_list(content.box(y=400))
        lst.item(show="next+").text("Vertices => tasks")
        lst.item(show="next+").text("Edges => dependencies")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Data movement", style="l2")

    @slides.slide()
    def task_runtime(slide: Box):
        content = slide_header_top(slide, "Task graph execution")

        task_start_center = 220
        task_size = 75
        t1 = task(content, task_start_center - 150, 100, name="t1", size=task_size)
        t2 = task(content, task_start_center + 50, 100, name="t2", size=task_size)
        t3 = task(content, task_start_center, 300, name="t3", size=task_size)
        t4 = task(content, task_start_center - 150, 300, name="t4", size=task_size)
        edge(content, task_point(t1, "50%", "50%"), task_point(t3, "25%", 0))
        edge(content, task_point(t2, "50%", "50%"), task_point(t3, "75%", 0))
        edge(content, task_bottom(t1), task_top(t4))

        runtime = content.box(width=250, height=80, y=140)
        runtime.rect(color="black")
        runtime.text("Task runtime")
        runtime.line((
            (runtime.x(-60), runtime.y("50%")),
            (runtime.x(-20), runtime.y("50%")),
        ), end_arrow=Arrow())
        runtime.line((
            (runtime.x("100%").add(20), runtime.y("50%")),
            (runtime.x("100%").add(60), runtime.y("50%")),
        ), end_arrow=Arrow())

        cluster_wrapper = content.box(y=40, x=700, width=250, height=150)
        cluster_wrapper.box().text("Cluster")
        cluster = cluster_wrapper.fbox(p_left=50, p_top=100)
        node(cluster, x=0, y=0, size=50)
        node(cluster, x=40, y=25, size=50)
        node(cluster, x=80, y=50, size=50)
        node(cluster, x=40, y=-25, size=50)
        node(cluster, x=80, y=0, size=50)
        node(cluster, x=80, y=-50, size=50)

        lst = unordered_list(content.box(p_top=120, show="next+"))
        lst.item().text("Bookkeeping")
        lst.item().text("Scheduling")

    @slides.slide()
    def workflows_tradeoffs(slide: Box):
        content = slide_header_top(slide, "Workflow trade-offs")

        lst = unordered_list(content.box())
        lst.item(label="+").text("High-level description")
        lst.item(label="+", show="next+").text("Implicit parallelism", TextStyle(bold=True))
        lst.item(label="+", show="next+").text("Portability")

        lst.item(label="-", show="next+", p_top=20).text("Iterative computations")
        lst.item(label="-", show="next+").text("Side effects/nondeterminism")
