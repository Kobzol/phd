from elsie import Arrow, Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from tasks import cluster_1, edge, task, task_bottom, task_graph_1, task_top
from utils import slide_header_top


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

        task_graph_1(content, size=75)

        lst = unordered_list(content.box(p_top=40))
        lst.item(show="next+").text("Vertices => tasks")
        lst.item(show="next+").text("Edges => dependencies")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Data movement", style="l2")

    @slides.slide()
    def task_runtime(slide: Box):
        content = slide_header_top(slide, "Task graph execution")

        row = content.box(horizontal=True)

        task_size = 75
        task_graph_1(row, size=task_size)

        runtime = row.box(width=300, height=60, p_left=60)
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

        cluster_wrapper = row.box(width=250, height=task_size * 3, p_left=60)
        cluster_wrapper.box().text("Cluster")
        cluster = cluster_wrapper.box(p_left=25)
        cluster_1(cluster, size=50)

        lst = unordered_list(content.box())
        lst.item(show="next+").text("Bookkeeping")
        lst.item(show="next+").text("Scheduling")

    @slides.slide()
    def workflows_tradeoffs(slide: Box):
        content = slide_header_top(slide, "Workflow trade-offs")

        lst = unordered_list(content.box())
        lst.item(label="+").text("High-level description")
        lst.item(label="+", show="next+").text("Implicit parallelism", TextStyle(bold=True))
        lst.item(label="+", show="next+").text("Portability")

        lst.item(label="-", show="next+", p_top=20).text("Iterative computations")
        lst.item(label="-", show="next+").text("Side effects/nondeterminism")
