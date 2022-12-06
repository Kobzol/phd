from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from tasks import cluster_1, get_task_color, half_node, node, task, task_graph_1, task_graph_grid
from utils import slide_header_top


def challenges(slides: Slides):
    @slides.slide()
    def job_manager_1(slide: Box):
        content = slide_header_top(slide, "Job manager")

        row = content.box(horizontal=True)
        task_graph_1(row, size=75)
        middle = row.box(width=50, p_left=25, p_right=25, show="next+")
        middle.image("images/brick-wall.jpeg")
        middle.text("PBS/Slurm", rotation=-90, style=TextStyle(color="white"))

        cluster_box = row.box()
        cluster_1(cluster_box, size=75)

        content.box(p_top=40, show="next+").text("How to map tasks to PBS jobs?")

    # @slides.slide()
    # def job_manager_granularity(slide: Box):
    #     content = slide_header_top(slide, "Granularity levels (task vs job)")
    #
    #     lst = unordered_list(content.box())
    #     lst.item().text("Duration")
    #     lst2 = lst.ul()
    #     lst2.item().text("Task: ms - hours", style="l2")
    #     lst2.item().text("Job: minutes - days", style="l2")
    #     lst.item(show="next+").text("Count")
    #     lst2 = lst.ul()
    #     lst2.item().text("Task: millions", style="l2")
    #     lst2.item().text("Job: hundreds", style="l2")
    #     lst.item(show="next+").text("Resource usage")
    #     lst2 = lst.ul()
    #     lst2.item().text("Task: cores, specific devices", style="l2")
    #     lst2.item().text("Job: nodes", style="l2")

    @slides.slide()
    def job_manager_submit(slide: Box):
        content = slide_header_top(slide, "Submitting task graphs into PBS")

        lst = unordered_list(content.box(x=50))
        lst.item(show="next+").text("Submit each task as a job")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Massive overhead (millions of jobs)", style="l2")
        lst2.item(show="next+").text("Job count limits", style="l2")
        lst2.item(show="next+").text("Node granularity", style="l2")
        lst2.item(show="next+").text("Difficult with dependencies", style="l2")
        lst.item(show="next+", p_top=30).text("Submit task graph as a single job")
        lst2 = lst.ul()
        lst2.item().text("Only for small-ish task graphs", style="l2")
        lst.item(show="next+", p_top=100).text("Split task graph into multiple jobs")
        lst2 = lst.ul()
        lst2.item().text("Lot of work", style="l2")
        lst2.item(show="next+").text("No load balancing across jobs", style="l2")
        lst2.item(show="next+").text("Complex bookkeeping", style="l2")

        task_size = 30
        node_size = 40

        def task_fn(box, x, y, name, size, row, col):
            task(box, x=x, y=y, name=None, size=size, bg_color=get_task_color(col))

        def tg(box: Box):
            task_graph_grid(box, size=task_size, rows=1, cols=3, task_constructor=task_fn)

        x_start = 700
        y_start = 150

        # Each task as a job
        box_1 = content.box(x=x_start, y=y_start, horizontal=True, show="2+")
        tg(box_1.box(p_right=40))
        nodes = cluster_1(box_1.box(), size=node_size)
        for (index, node_box) in enumerate(nodes[:3]):
            node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                 bg_color=get_task_color(index))

        # Task graph as a single job
        box_1 = content.box(x=x_start, y=y_start + 180, horizontal=True, show="7+")
        tg(box_1.box(p_right=40))
        nodes = cluster_1(box_1.box(), size=node_size)
        node_box = nodes[0]
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(0))
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(1), mode="down")
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(2), mode="left")

        # Split graph
        box_1 = content.box(x=x_start, y=y_start + 340, horizontal=True, show="8+")
        tg(box_1.box(p_right=40))
        nodes = cluster_1(box_1.box(), size=node_size)
        node_box = nodes[0]
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(0))
        half_node(node_box.overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
                  bg_color=get_task_color(1), mode="down")
        node(nodes[1].overlay(), x=node_size / 2, y=node_size / 2, size=node_size,
             bg_color=get_task_color(2))

    @slides.slide()
    def heterogeneity(slide: Box):
        content = slide_header_top(slide, "Resource management")
        line_box = content.overlay(show="2+")

        nodes = cluster_1(content.box(x=50, y=300), size=40)
        node = nodes[5]
        line_box.line((
            (node.x("25%"), node.y(0)),
            (385, 175)
        ), stroke_width=2, stroke_dasharray="4")
        line_box.line((
            (node.x("25%"), node.y("100%")),
            (385, 530)
        ), stroke_width=2, stroke_dasharray="4")

        content.box(width="75%").image("images/heterogeneous-node.svg", show_begin=2)

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
