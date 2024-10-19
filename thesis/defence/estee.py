from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def estee(slides: Slides):
    @slides.slide()
    def estee_intro(slide: Box):
        slide.box().text("Analysis of workflow schedulers in\nsimulated distributed environments")
        slide.box(p_top=10).text("Jakub Beránek, Stanislav Böhm, Vojtěch Cima", style=TextStyle(size=20))
        slide.box().text("(The Journal of Supercomputing 2022)", style=TextStyle(size=20))

        paper_box = slide.box(x=10, y=10, width=160)
        paper_box.rect(color="black", stroke_width=2)
        paper_box.image("images/estee-paper.png")

        slide.update_style("default", TextStyle(size=30))
        lst = unordered_list(slide.box(p_top=40))
        lst.item(show="next+").text("Compare scheduler performance")
        lst.item(show="next+").text("Analyze neglected factors")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Delay between scheduling", style="l2")
        lst2.item(show="next+").text("Knowledge about task durations", style="l2")
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
