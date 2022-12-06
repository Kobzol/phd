from elsie import Arrow, Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from tasks import task_graph_3
from utils import slide_header_top


def workflows(slides: Slides):
    @slides.slide()
    def workflows_definition(slide: Box):
        content = slide_header_top(slide, "Workflows")

        lst = unordered_list(content.box())
        lst.item(label="=").text("task graphs, pipelines, task DAGs*, …")
        content.box(show="next+", p_top=40, ).text("Popular programming model")

        nodes = task_graph_3(content.box(width=400, height=300, show="last+"), size=70)

        node = nodes[3]
        wrapper = content.overlay(show="3+")
        text_box = wrapper.box(x=700, y=450).text("Function or binary", style=TextStyle(size=26))
        wrapper.line((
            (text_box.x(0).add(-10), text_box.y("50%")),
            (node.x("100%"), node.y("50%"))
        ), stroke_dasharray="4", end_arrow=Arrow())

        wrapper = content.overlay(show="4+")
        text_box = wrapper.box(x=700, y=550).text("~tt{t5} can't start\nbefore ~tt{t4} finishes",
                                                  style=TextStyle(size=26, align="left"))
        wrapper.line((
            (text_box.x(0).add(-10), text_box.y("50%")),
            (node.x(0).add(5), node.y("100%").add(30))
        ), stroke_dasharray="4", end_arrow=Arrow())

        content.box(x=20, y=600).text("* Directed Acyclic Graph", style=TextStyle(size=20))

    @slides.slide()
    def workflows_tradeoffs(slide: Box):
        content = slide_header_top(slide, "Main workflow benefits")

        lst = unordered_list(content.box())
        lst.item().text("Implicit parallelism", style="bold")
        lst2 = lst.ul()
        lst2.item().text("Build a DAG vs use MPI", style="l2")
        lst2.item(show="next+").text("Extracted by a task runtime", style="l2")
        lst.item(show="next+").text("High-level description")
        lst2 = lst.ul()
        lst2.item().text("Python/DSL vs C/C++", style="l2")
        lst.item(show="next+").text("Portability")
        lst2 = lst.ul()
        lst2.item().text("Use-cases, hardware", style="l2")

        # lst.item(label="-", show="next+", p_top=20).text("Iterative computations")
        # lst.item(label="-", show="next+").text("Side effects/nondeterminism")
