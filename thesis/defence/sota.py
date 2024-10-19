from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def sota(slides: Slides):
    @slides.slide()
    def task_duration(slide: Box):
        content = slide_header_top(slide, "State of the art: task duration")
        content.box(width="80%").image("images/sota.svg")

    @slides.slide()
    def task_duration(slide: Box):
        content = slide_header_top(slide, "State of the art: job manager")
        content.box(width="80%").image("images/sota-pbs.svg")

    @slides.slide()
    def other(slide: Box):
        content = slide_header_top(slide, "State of the art: resources & multi-node")
        lst = unordered_list(content.box())
        lst.item().text("Resource requirements: ✓ (simple)")
        lst.item(show="next+").text("Multi-node tasks: x")

    # @slides.slide()
    # def sota_table(slide: Box):
    #     content = slide_header_top(slide, "State of the Art")
    #     # Dask, Ray, Nextflow, Snakemake, PyCompss, Parsl
    #
    #     nodes = {}
    #     width = 180
    #     height = 60
    #     headers = ["", "PBS/Slurm", "Resources", "Multi-node", "tasks/s"]
    #     data = [
    #         ["Dask", "plugin", "+", "-", "medium"],
    #         ["Ray", "-", "+", "-", "high"],
    #         ["Snakemake", "+", "+", "-", "low"],
    #     ]
    #
    #     rows = len(data) + 1
    #     cols = len(headers)
    #
    #     table = content.box()
    #     table.update_style("default", style=TextStyle(size=24))
    #     for row in range(rows):
    #         row_box = table.box(horizontal=True)
    #         for col in range(cols):
    #             node = row_box.box(width=width, height=height)
    #             node.rect(color="black")
    #             nodes[(row, col)] = node
    #     for (header, col) in zip(headers, range(cols)):
    #         node = nodes[(0, col)]
    #         node.text(header, style=TextStyle(bold=True))
    #
    #     for (row, items) in enumerate(data):
    #         for (col, item) in enumerate(items):
    #             nodes[(row + 1, col)].overlay(show=f"{row + 2}+").text(item)
    #
    #     lst = unordered_list(content.box(show="next+", p_top=50))
    #     lst.item().text("Simplistic resource management")
    #     lst.item(show="next+").text("No support for multinode tasks")
    #     lst.item(show="next+").text("May be inefficient (Dask, Snakemake)")
