from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import github_link, slide_header_top


def rsds(slides: Slides):
    @slides.slide()
    def rsds_intro(slide: Box):
        rows = slide.box(x=50, horizontal=True)
        paper_box = rows.box(p_right=80).box(width=500)
        paper_box.rect(color="black", stroke_width=4)
        paper_box.image("images/rsds-paper.png")

        box = rows.box(y=0)
        box.box().text("Runtime vs Scheduler:\nAnalyzing Dask’s Overheads")
        size = 30
        box.box(p_top=20).text("Ada Böhm, Jakub Beránek", style=T(size=size))
        box.box().text("(IEEE/ACM Workflows in Support of Large-Scale Science 2020)", style=T(size=size))

        box.update_style("default", T(size=40))
        lst = unordered_list(box.box(p_top=60))
        lst.item(show="next+").text('How do schedulers perform "in the wild"?')
        lst.item(show="next+").text("What are the perf. characteristics of Dask?")
        lst.item(show="next+").text("Can we make Dask more efficient on HPC?")

    @slides.slide()
    def estee_validation(slide: Box):
        content = slide_header_top(slide, "Validation of ESTEE results")
        content.box(width="90%").image("images/estee-validation.png")

    @slides.slide()
    def dask_random_scheduler(slide: Box):
        content = slide_header_top(slide, "Random vs. work-stealing scheduler")
        content.box(width="80%").image("images/speedup-dask-random-7.png")

    @slides.slide()
    def dask_scaling(slide: Box):
        content = slide_header_top(slide, "Dask scaling")
        content.box(width="80%").image("images/dask-strong-scaling.svg", fragments=False)

    @slides.slide()
    def dask_gil_scaling(slide: Box):
        content = slide_header_top(slide, "Effect of GIL on Dask's performance")
        content.box(width="45%").image("images/dask-gil-scaling.svg", fragments=False)

    @slides.slide()
    def dask_observations(slide: Box):
        content = slide_header_top(slide, "Observations")
        lst = unordered_list(content.box())
        lst.item(show="next+").text("Scheduler cannot be easily replaced")
        lst.item(show="next+").text("Dask does not scale well in HPC contexts")
        lst.item(show="next+").text("Python implementation is limited by the GIL")

    @slides.slide()
    def rsds(slide: Box):
        content = slide_header_top(slide, "RSDS")
        lst = unordered_list(content.box())
        lst.item(show="next+").text("Alternative Dask server implementation")
        lst.item(show="next+").text("Written in Rust, designed for low overhead")
        lst.item(show="next+").text("Explicitly designed for a pluggable scheduler")

    @slides.slide()
    def rsds_architecture(slide: Box):
        content = slide_header_top(slide, "RSDS architecture")
        content.box(width="80%").image("images/rsds-architecture.png")

    @slides.slide()
    def rsds_dask(slide: Box):
        content = slide_header_top(slide, "Dask vs. RSDS: work-stealing scheduler")
        content.box(width="70%").image("images/rsds-dask-ws.png")

    @slides.slide()
    def rsds_scaling(slide: Box):
        content = slide_header_top(slide, "Dask vs. RSDS: scaling")
        content.box(width="70%", p_top=80).image("images/rsds-scaling.png")

    @slides.slide()
    def rsds_outcome(slide: Box):
        content = slide_header_top(slide, "Outcome")
        lst = unordered_list(content.box())
        lst.item().text("Runtime efficiency as important as scheduling")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Even a random scheduler can be competitive!", style="l2")
        lst.item(show="next+").text("Dask scaled poorly on HPC")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Caused by inefficient runtime and GIL", style="l2")
        lst2.item(show="next+").text("<100 ms tasks problematic", style="l2")
        lst.item(show="next+").text("RSDS: open source alternative to Dask's server")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Backward-compatible with existing Dask programs", style="l2")
        github_link(lst2.item(show="last+"), "github.com/it4innovations/rsds", style="l2")
        lst.item(show="next+").text("Some ideas from RSDS were integrated into Dask")
