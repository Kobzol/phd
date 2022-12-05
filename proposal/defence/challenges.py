from elsie import Arrow, Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from tasks import cluster_1, task_graph_1
from utils import slide_header_top


def challenges(slides: Slides):
    @slides.slide()
    def job_manager_1(slide: Box):
        content = slide_header_top(slide, "Job manager")

        row = content.box(horizontal=True)
        task_graph_1(row, size=75)
        middle = row.box(width=50, p_left=25, p_right=25)
        middle.image("images/brick-wall.jpeg")
        middle.text("PBS/Slurm", rotation=-90, style=TextStyle(color="white"))

        cluster_box = row.box()
        cluster_1(cluster_box, size=75)

    @slides.slide()
    def job_manager_granularity(slide: Box):
        content = slide_header_top(slide, "Granularity levels (task vs job)")

        lst = unordered_list(content.box())
        lst.item().text("Duration")
        lst2 = lst.ul()
        lst2.item().text("Task: ms - hours", style="l2")
        lst2.item().text("Job: minutes - days", style="l2")
        lst.item(show="next+").text("Count")
        lst2 = lst.ul()
        lst2.item().text("Task: millions", style="l2")
        lst2.item().text("Job: hundreds", style="l2")
        lst.item(show="next+").text("Resource usage")
        lst2 = lst.ul()
        lst2.item().text("Task: cores, specific devices", style="l2")
        lst2.item().text("Job: nodes", style="l2")

    @slides.slide()
    def job_manager_submit(slide: Box):
        content = slide_header_top(slide, "Workflows + PBS/Slurm")

        lst = unordered_list(content.box())
        lst.item(show="next+").text("Submit workflow as a single job")
        lst2 = lst.ul()
        lst2.item().text("Only for small-ish workflows", style="l2")
        lst.item(show="next+").text("Submit each task as a job")
        lst2 = lst.ul()
        lst2.item().text("Massive overhead", style="l2")
        lst2.item().text("Job count limits", style="l2")
        lst.item(show="next+").text("Split workflow into multiple jobs")
        lst2 = lst.ul()
        lst2.item().text("(Semi)-manual work", style="l2")
        lst2.item().text("Nonoptimal load balancing", style="l2")

    @slides.slide()
    def heterogeneity(slide: Box):
        content = slide_header_top(slide, "Other workflow challenges on HPC")

        lst = unordered_list(content.box())
        lst.item().text("Cluster heterogeneity")
        lst.item(show="next+").text("Data transfers between tasks")
        lst.item(show="next+").text("Fault tolerance")
        lst.item(show="next+").text("Scalability")
        lst.item(show="next+").text("Multi-node tasks")
        lst.item(show="next+").text("Iterative computation")
