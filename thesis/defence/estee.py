from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textboxitem import TextBoxItem

from utils import code_step, github_link, slide_header_top


def estee(slides: Slides):
    @slides.slide()
    def estee_intro(slide: Box):
        rows = slide.box(x=50, horizontal=True)
        paper_box = rows.box(p_right=50).box(width=400)
        paper_box.rect(color="black", stroke_width=4)
        paper_box.image("images/estee-paper.png")

        box = rows.box(y=0)
        box.box().text("Analysis of workflow schedulers in\nsimulated distributed environments")
        size = 30
        box.box(p_top=20).text("Jakub Beránek, Ada Böhm, Vojtěch Cima", style=T(size=size))
        box.box().text("(The Journal of Supercomputing 2022)", style=T(size=size))

        box.update_style("default", T(size=40))
        lst = unordered_list(box.box(p_top=80))
        lst.item(show="next+").text("Which scheduling algorithms are the best for HPC?")
        lst.item(show="next+").text("Which factors affect scheduling the most?")
        lst.item(show="next+").text("How can we simplify scheduler prototyping?")

    @slides.slide()
    def estee_code(slide: Box):
        slide = slide_header_top(slide, "ESTEE")

        slide.update_style("default", T(size=50))
        lst = unordered_list(slide.box())
        lst.item().text("Framework for simulating task graph execution")
        # Discrete event simulation
        lst.item(show="next+").text("Python interface designed for prototyping")
        lst.item(show="next+").text('"Batteries included"')

    @slides.slide()
    def estee_code(slide: Box):
        slide = slide_header_top(slide, "ESTEE usage example")
        slide.update_style("code", T(size=26))

        row = slide.box(horizontal=True, x=25, p_top=100)
        width = 1030
        codebox: TextBoxItem = code_step(row.box(p_top=30, width=width, y=0), """
dag = TaskGraph()
t0 = dag.new_task(duration=1, cpus=1, output_size=50)
t1 = dag.new_task(duration=1, cpus=1)
t1.add_input(t0)
t2 = dag.new_task(duration=1, cpus=1)
t2.add_input(t0)

scheduler = BlevelGtScheduler()
cluster   = [Worker(cpus=8) for _ in range(3)]
network   = MaxMinFlowNetModel(bandwidth=10*1024)

simulator = Simulator(task_graph, cluster, scheduler, network)
~#makespan{makespan}  = simulator.run()
""", 1, [
            list(range(6)),
            list(range(8)),
            list(range(9)),
            list(range(10)),
            list(range(13)),
        ], language="python", width=width, use_styles=True, return_box=True)
        row.box(width=30)
        row.box(width=500).image("images/estee-architecture.svg")
        codebox.inline_box("#makespan", padding=-5, show="next+").rect(color="red", stroke_width=4)

    @slides.slide()
    def estee_analysis(slide: Box):
        slide = slide_header_top(slide, "Scheduler analysis")

        slide.update_style("default", T(size=45))
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Compare scheduler performance")
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
    def estee_outcome(slide: Box):
        content = slide_header_top(slide, "Outcome")
        lst = unordered_list(content.box())
        lst.item().text("Most competitive schedulers")
        lst2 = lst.ul()
        lst2.item(show="next+").text("B-level", style="l2")
        lst2.item(show="next+").text("Work-stealing", style="l2")
        lst.item(show="next+").text("Implementation details matter a lot!")
        lst.item(show="next+").text("Open source scheduler simulator ESTEE")
        lst2 = lst.ul()
        github_link(lst2.item(show="last+"), "github.com/it4innovations/estee", style="l2")
        lst2.item(show="next+").text("Benchmark datasets and results @ Zenodo", style="l2")
