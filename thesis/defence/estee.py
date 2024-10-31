from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import code_step, slide_header_top


def estee(slides: Slides):
    @slides.slide()
    def estee_intro(slide: Box):
        box = slide.box()
        box.box().text("Analysis of workflow schedulers in\nsimulated distributed environments")
        size = 30
        box.box(p_top=20).text("Jakub Beránek, Stanislav Böhm, Vojtěch Cima", style=T(size=size))
        box.box().text("(The Journal of Supercomputing 2022)", style=T(size=size))

        paper_box = slide.box(x=20, y=20, width=300)
        paper_box.rect(color="black", stroke_width=4)
        paper_box.image("images/estee-paper.png")

        slide.update_style("default", T(size=40))
        lst = unordered_list(slide.box(p_top=80))
        lst.item(show="next+").text("Scheduler experimentation framework")
        lst.item(show="next+").text("Comparison of scheduler performance")
        lst.item(show="next+").text("Analyze neglected factors")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Knowledge about task durations", style="l2")
        lst2.item(show="next+").text("Delay between scheduling", style="l2")
        lst2.item(show="next+").text("Network model", style="l2")

    @slides.slide()
    def estee_code(slide: Box):
        slide.box(y=20).text("ESTEE: scheduler experimentation framework")

        slide.update_style("code", T(size=30))
        width = 1000
        code_step(slide.box(p_top=40, width=width, y="[10%]"), """
# Create task graph containing 3 tasks
# (each task runs 1s and requires 1 CPU)
#
#     t0
#     | (50MB output)
#    / \\
#  t1   t2
task_graph = TaskGraph()
t0 = task_graph.new_task(duration=1, cpus=1, output_size=50)
t1 = task_graph.new_task(duration=1, cpus=1)
t1.add_input(t0)
t2 = task_graph.new_task(duration=1, cpus=1)
t2.add_input(t0)

scheduler = BlevelGtScheduler()
cluster = [Worker(cpus=1) for _ in range(2)]
netmodel = MaxMinFlowNetModel(bandwidth=100)

simulator = Simulator(task_graph, cluster, scheduler, netmodel)
makespan = simulator.run()
""", 1, [
            list(range(7))
        ], language="python", width=width)

    @slides.slide()
    def estee_plan(slide: Box):
        slide.update_style("default", T(size=40))
        lst = unordered_list(slide.box(p_top=80))
        lst.item(show="next+").text("Scheduler experimentation framework")
        lst.item(show="next+").text("Comparison of scheduler performance")
        lst.item(show="next+").text("Analyze neglected factors")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Knowledge about task durations", style="l2")
        lst2.item(show="next+").text("Delay between scheduling", style="l2")
        lst2.item(show="next+").text("Network model", style="l2")

    @slides.slide()
    def estee_chart_1(slide: Box):
        content = slide_header_top(slide, "Runtime vs. network speed")
        content.box(width="75%").image("images/estee-network.png")

    @slides.slide()
    def estee_chart_2(slide: Box):
        content = slide_header_top(slide, "Scheduling delay effect")
        content.box(width="75%").image("images/estee-msd.png")

    @slides.slide()
    def estee_outcomes(slide: Box):
        content = slide_header_top(slide, "Outcome")
        lst = unordered_list(content.box())
        lst.item().text("Most competitive schedulers")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Work-stealing (used in Dask)", style="l2")
        lst2.item(show="next+").text("B-level (basic heuristic)", style="l2")
        lst.item(show="next+").text("Implementation details matter a lot!")
        lst.item(show="next+").text("Open source scheduler simulator ESTEE")
        lst2 = lst.ul()
        lst2.item(show="last+").text("~tt{github.com/it4innovations/estee}", style="l2")
