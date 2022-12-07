from typing import List, Optional, Tuple, Union

import seaborn as sns
from elsie import Arrow, TextStyle
from elsie.boxtree.box import Box


def task(box: Box, x=0, y=0, size=100, name: Optional[str] = None,
         style: Union[str, TextStyle] = "default", bg_color="white",
         show: Optional[str] = None) -> Box:
    box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, z_level=2, show=show)
    box.rect(color="black", bg_color=bg_color, stroke_width=4, rx=100, ry=100)
    if name is not None:
        box.text(name, style=style)
    return box


def draw_node(box: Box, color="black", bg_color: Optional[str] = None, **kwargs):
    box.polygon([
        (box.x("25%"), box.y(0)),
        (box.x("75%"), box.y(0)),
        (box.x("100%"), box.y("50%")),
        (box.x("75%"), box.y("100%")),
        (box.x("25%"), box.y("100%")),
        (box.x(0), box.y("50%")),
    ], color=color, bg_color=bg_color, **kwargs)


def node(box: Box, x=0, y=0, size=30, color="black", bg_color: Optional[str] = None,
         node_args=None, **box_args) -> Box:
    node_box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, **box_args)
    node_args = {} if node_args is None else node_args
    draw_node(node_box, color=color, bg_color=bg_color, **node_args)
    return node_box


def half_node(box: Box, x: int, y: int, size=30, color="black", bg_color: Optional[str] = None,
              node_args=None, mode: str = "up", **box_args):
    node_box = box.box(x=x - size / 2, y=y - size / 2, width=size, height=size, **box_args)
    node_args = {} if node_args is None else node_args
    if mode == "up":
        node_box.polygon([
            (box.x("25%"), box.y(0)),
            (box.x("75%"), box.y(0)),
            (box.x("100%"), box.y("50%")),
            (box.x(0), box.y("50%")),
        ], color=color, bg_color=bg_color, **node_args)
    elif mode == "down":
        node_box.polygon([
            (box.x("100%"), box.y("50%")),
            (box.x("75%"), box.y("100%")),
            (box.x("25%"), box.y("100%")),
            (box.x(0), box.y("50%")),
        ], color=color, bg_color=bg_color, **node_args)
    elif mode == "left":
        node_box.polygon([
            (box.x("25%"), box.y(0)),
            (box.x("50%"), box.y(0)),
            (box.x("50%"), box.y("100%")),
            (box.x("25%"), box.y("100%")),
            (box.x(0), box.y("50%")),
        ], color=color, bg_color=bg_color, **node_args)
    else:
        assert False


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


def task_graph_1(box: Box, size: int, with_names=True) -> Tuple[Box, Box, Box, Box]:
    dim = size * 3
    box = box.box(width=dim, height=dim)

    y = size / 2
    x = size / 2

    style = TextStyle(size=size / 2)
    t1 = task(box, x, y, name="t1" if with_names else None, size=size, style=style)
    t2 = task(box, x + size * 2, y, name="t2" if with_names else None, size=size, style=style)
    t3 = task(box, x, y + size * 2, name="t3" if with_names else None, size=size, style=style)
    t4 = task(box, x + size * 2, y + size * 2, name="t4" if with_names else None, size=size,
              style=style)
    edge(box, task_point(t1, "50%", "50%"), task_top(t3))
    edge(box, task_point(t1, "50%", "50%"), task_point(t4, "25%", 0))
    edge(box, task_point(t2, "50%", "50%"), task_top(t4))

    return (t1, t2, t3, t4)


def task_graph_2(box: Box, size: int, task_constructor=None) -> List[Box]:
    box = box.box(width=size * 3, height=size * 2)

    y = size / 2

    if task_constructor is None:
        task_constructor = lambda box, x, y, name, size, **kwargs: task(box=box, x=x, y=y,
                                                                        name=name,
                                                                        size=size,
                                                                        style=TextStyle(
                                                                            size=size / 2))

    margin = size * 0.2
    index = 1
    tasks = []
    for row in range(2):
        x = size / 2
        for col in range(3):
            task_box = task_constructor(box=box, x=x, y=y, name=f"t{index}", size=size, row=row,
                                        col=col)
            tasks.append(task_box)
            x += size + margin
            index += 1
        y += size + margin
    return tasks


def task_graph_grid(box: Box, size: int, rows: int, cols: int, task_constructor=None) -> List[Box]:
    margin = size * 0.2
    box = box.box(width=size * cols + margin * (cols - 1), height=size * rows + margin * (rows - 1))

    y = size / 2

    if task_constructor is None:
        task_constructor = lambda box, x, y, name, size, **kwargs: task(box=box, x=x, y=y,
                                                                        name=name,
                                                                        size=size,
                                                                        style=TextStyle(
                                                                            size=size / 2))

    index = 1
    tasks = []
    for row in range(rows):
        x = size / 2
        for col in range(cols):
            task_box = task_constructor(box=box, x=x, y=y, name=f"t{index}", size=size, row=row,
                                        col=col)
            tasks.append(task_box)
            x += size + margin
            index += 1
        y += size + margin
    return tasks


def task_graph_3(box: Box, size: int) -> Tuple[Box, Box, Box, Box]:
    dim = size * 3
    box = box.box(width=dim, height=dim)

    y = size / 2
    x = size / 2

    style = TextStyle(size=size / 2)
    t1 = task(box, x, y, name="t1", size=size, style=style)
    t2 = task(box, x + size * 2, y, name="t2", size=size, style=style)
    t3 = task(box, x, y + size * 2, name="t3", size=size, style=style)
    t4 = task(box, x + size * 2, y + size * 2, name="t4", size=size, style=style)
    t5 = task(box, x + size, y + size * 4, name="t5", size=size, style=style)
    edge(box, task_point(t1, "50%", "50%"), task_top(t3))
    edge(box, task_point(t1, "50%", "50%"), task_point(t4, "25%", 0))
    edge(box, task_point(t2, "50%", "50%"), task_top(t4))
    edge(box, task_point(t3, "50%", "50%"), task_point(t5, "25%", 0))
    edge(box, task_point(t4, "50%", "50%"), task_point(t5, "75%", 0))

    return (t1, t2, t3, t4)


def cluster_1(box: Box, size: int, node_constructor=None, **box_args) -> List[Box]:
    height = size * 3
    box = box.box(width=size * 3, height=height, **box_args)
    x_increment = size * 0.8
    y_increment = size / 2

    if node_constructor is None:
        node_constructor = lambda box, x, y, size, diagonal, index: node(box, x=x, y=y, size=size)

    nodes = []
    for diagonal in range(3):
        items = 3 - diagonal
        x = size / 2 + (x_increment * diagonal)
        y = (height * 0.5) - (y_increment * diagonal)

        for index in range(items):
            node_box = node_constructor(box=box, x=x, y=y, size=size, diagonal=diagonal,
                                        index=index)
            nodes.append(node_box)
            x += x_increment
            y += y_increment
    return nodes


def get_task_color(index: Union[int, str]) -> str:
    if isinstance(index, str):
        return index
    return sns_to_elsie_color(sns.color_palette()[index])


def sns_to_elsie_color(color: Tuple[float, float, float]) -> str:
    color = tuple(int(v * 255) for v in color)
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()
