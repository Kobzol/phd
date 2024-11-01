from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def rsds(slides: Slides):
    @slides.slide()
    def rsds_intro(slide: Box):
        slide.box().text("Runtime vs Scheduler: Analyzing Dask’s Overheads")
        slide.box(p_top=10).text("Ada Böhm, Jakub Beránek", style=TextStyle(size=20))
        slide.box().text("(IEEE/ACM Workflows in Support of Large-Scale Science 2020)",
                         style=TextStyle(size=20))

        paper_box = slide.box(x=10, y=10, width=180)
        paper_box.rect(color="black", stroke_width=2)
        paper_box.image("images/rsds-paper.png")

        slide.update_style("default", TextStyle(size=30))
        lst = unordered_list(slide.box(p_top=40))
        lst.item(show="next+").text('Test schedulers "in the wild"')
        lst.item(show="next+").text("Analyze Dask's performance on HPC")
        lst.item(show="next+").text("Implement more efficient Dask server (RSDS)")
        lst2 = lst.ul()
        lst2.item().text("Pluggable scheduler", style="l2")

    @slides.slide()
    def rsds_dask(slide: Box):
        content = slide_header_top(slide, "Dask vs. RSDS: work-stealing scheduler")
        content.box(width="80%").image("images/rsds-dask-ws.png")

    @slides.slide()
    def dask_random(slide: Box):
        content = slide_header_top(slide, "Dask vs. RSDS: scaling on Salomon")
        content.box(width="90%").image("images/rsds-scaling.png")

    @slides.slide()
    def rsds_summary(slide: Box):
        content = slide_header_top(slide, "Outcome")
        lst = unordered_list(content.box())
        lst.item().text("Runtime efficiency as important as scheduling")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Even a random scheduler can be competitive!", style="l2")
        lst.item(show="next+").text("Dask scaled poorly on HPC")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Caused by inefficient runtime", style="l2")
        lst2.item(show="next+").text("<100 ms tasks problematic", style="l2")
        lst.item(show="next+").text("RSDS: open source alternative to Dask's server")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Backward-compatible with existing Dask programs", style="l2")
        lst2.item(show="last+").text("~tt{github.com/it4innovations/rsds}", style="l2")
