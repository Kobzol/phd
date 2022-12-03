from typing import Optional, Tuple, Union

from elsie import Arrow, TextStyle
from elsie.boxtree.box import Box


def task(box: Box, x: int, y: int, size=100, name: Optional[str] = None,
         style: Union[str, TextStyle] = "default") -> Box:
    box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, z_level=2)
    box.rect(color="black", bg_color="white", stroke_width=4, rx=100, ry=100)
    if name is not None:
        box.text(name, style=style)
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


def task_graph_1(box: Box, task_size: int) -> Tuple[Box, Box, Box, Box]:
    dim = task_size * 3
    box = box.box(width=dim, height=dim)

    y = task_size / 2
    x = task_size / 2

    style = TextStyle(size=task_size / 2)
    t1 = task(box, x, y, name="t1", size=task_size, style=style)
    t2 = task(box, x + task_size * 2, y, name="t2", size=task_size, style=style)
    t3 = task(box, x, y + task_size * 2, name="t3", size=task_size, style=style)
    t4 = task(box, x + task_size * 2, y + task_size * 2, name="t4", size=task_size, style=style)
    edge(box, task_point(t1, "50%", "50%"), task_top(t3))
    edge(box, task_point(t1, "50%", "50%"), task_point(t4, "25%", 0))
    edge(box, task_point(t2, "50%", "50%"), task_top(t4))

    return (t1, t2, t3, t4)


def cluster_1(box: Box, size: int, **box_args):
    height = size * 3
    box = box.box(width=size*3, height=height, **box_args)
    x_increment = size * 0.8
    y_increment = size / 2

    for diagonal in range(3):
        items = 3 - diagonal
        x = size / 2 + (x_increment * diagonal)
        y = (height * 0.5) - (y_increment * diagonal)

        for _ in range(items):
            node(box, x=x, y=y, size=size)
            x += x_increment
            y += y_increment
