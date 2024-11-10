from elsie import Arrow, Slides, TextStyle as T
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
        text_box = wrapper.box(x="[80%]", y="[70%]").text("Function or binary", style=T(size=32))
        wrapper.line((
            (text_box.x(0).add(-10), text_box.y("50%")),
            (node.x("100%"), node.y("50%"))
        ), stroke_dasharray="4", stroke_width=4, end_arrow=Arrow())

        node = nodes[2]
        wrapper = content.overlay(show="4+")
        text_box = wrapper.box(x="[25%]", y="[75%]").text("~tt{t5} cannot start\nbefore ~tt{t3} finishes",
                                                  style=T(size=32, align="left"))
        wrapper.line((
            (text_box.x("100%"), text_box.y("50%")),
            (node.x("100%").add(-5), node.y("100%").add(30))
        ), stroke_dasharray="4", stroke_width=4, end_arrow=Arrow())

        content.box(x="[90%]", y="[95%]").text("* Directed Acyclic Graph", style=T(size=40))

    @slides.slide()
    def workflows_tradeoffs(slide: Box):
        content = slide_header_top(slide, "Benefits of task-based programming")

        lst = unordered_list(content.box())
        lst.item().text("Implicit parallelism", style="bold")
        lst2 = lst.ul()
        lst2.item().text("Create a DAG vs. explicit MPI calls", style="l2")
        lst2.item().text("Extracted by a task runtime", style="l2")
        lst.item(show="next+", p_top=40).text("High-level description")
        lst2 = lst.ul()
        lst2.item().text("Python/DSL vs. C/C++", style="l2")
        lst.item(show="next+", p_top=40).text("Portability")

        # lst.item(label="-", show="next+", p_top=20).text("Iterative computations")
        # lst.item(label="-", show="next+").text("Side effects/nondeterminism")
