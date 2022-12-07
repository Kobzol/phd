from typing import List, Optional

import elsie
from elsie import Arrow
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.text.textstyle import TextStyle, TextStyle as T

from challenges import challenges
from estee import estee
from hq import hyperqueue
from rsds import rsds
from sota import sota
from tasks import cluster_1, task_graph_1
from utils import slide_header_top
from workflows import workflows

slide_width = 1024
slide_height = 768

slides = elsie.Slides(width=slide_width, height=slide_height)
slides.update_style("default", T(font="Raleway", size=36, variant_numeric="lining-nums"))
slides.set_style("l2", T(size=30))
slides.set_style("bold", T(bold=True))
slides.set_style("emph", T(italic=True))


@slides.slide()
def intro(slide: Box):
    slide.box().text("""Ergonomics and efficiency
of workflows on HPC clusters""", style=T(size=48))
    slide.box(p_top=40).text("Jakub Beránek")

    style = T(align="left", size=28)
    supervisor = slide.box(x="5%", y="80%")
    supervisor.box(width=400).text("Supervisor", style=style)
    supervisor.box(width=400).text("Ing. Jan Martinovič, Ph.D.", style=style.compose(T(bold=True)))

    slide.box(x="58%", y="80%", width=400).image("images/it4i-logo.png")


# @slides.slide()
# def intro(slide: Box):
#     content = slide_header(slide, "Outline")
#     lst = ordered_list(content.box())
#     lst.item().text("HPC & task graphs")
#     lst.item().text("HyperQueue")
#     lst.item().text("Distributed systems research")
#     lst.item().text("Next steps")
#     lst.item().text("Publications")


@slides.slide()
def goal(slide: Box):
    content = slide
    content.box(p_bottom=80).text("""Ergonomics and efficiency
of workflows on HPC clusters""", style=TextStyle(size=48))
    content.box().text("Goal", style="bold")
    content.box().text("""Help users execute task workflows
on HPC clusters in an easy & efficient way""")

    row = content.box(horizontal=True, p_top=40)
    task_graph_1(row.box(show="next+"), size=75)
    middle = row.box(width=50, height=50, p_left=75, p_right=75, show="next+")
    middle.box().line((
        (middle.x(0).add(-40), middle.y("50%")),
        (middle.x("100%").add(40), middle.y("50%"))
    ), end_arrow=Arrow(), stroke_width=4)
    cluster_box = row.box(show="last+")
    cluster_1(cluster_box, size=75)


@slides.slide()
def objectives(slide: Box):
    content = slide_header_top(slide, "Objectives")
    lst = ordered_list(content.box())
    lst.item().text("Identify HPC workflow challenges")
    lst.item(show="next+").text("Design approaches for overcoming them")
    lst.item(show="next+").text("Implement them in a task runtime")
    lst.item(show="next+").text("Analyze results on real use-cases")


def topic_highlight(slides: elsie.Slides, text: str, header: Optional[str] = None):
    slide = slides.new_slide()
    slide.set_style("highlight", T(bold=True))
    if header is not None:
        content = slide_header_top(slide, header)
    else:
        content = slide
    content.box().text(text, style=T(size=48))


topic_highlight(slides, """Ergonomics and efficiency
of ~highlight{workflows on HPC clusters}""", header="Motivation")

workflows(slides)


@slides.slide()
def task_graph_challenges(slide: Box):
    slide.box().text("Task graph challenges on HPC clusters", style=TextStyle(size=46))


challenges(slides)
sota(slides)

topic_highlight(slides, """Ergonomics and ~highlight{efficiency}
of workflows on HPC clusters""")

estee(slides)
rsds(slides)

topic_highlight(slides, """~highlight{Ergonomics} and efficiency
of workflows on HPC clusters""")

hyperqueue(slides)


@slides.slide()
def next_steps(slide: Box):
    content = slide_header_top(slide, "Objectives + plan")

    lst = unordered_list(content.box())
    lst.item().text("Identify HPC workflow challenges ✓")
    lst.item(show="next+").text("Analyze efficiency")
    lst2 = lst.ul()
    lst2.item(show="next+").text("Schedulers ✓", style="l2")
    lst2.item(show="next+").text("Dask ✓", style="l2")
    lst2.item(show="next+").text("~bold{HyperQueue performance study} •", style="l2")
    lst.item(show="next+").text("Analyze ergonomics")
    lst2 = lst.ul()
    lst2.item(show="next+").text("HyperQueue ✓", style="l2")
    lst2.item(show="next+").text("~bold{Automatic allocation analysis} •", style="l2")
    # lst.item(show="next+").text("Formalize HQ task semantics ?")
    lst.item(show="next+").text("Prepare HyperQueue publication")


@slides.slide()
def publications_related(slide: Box):
    slide.box().text("Publications related to thesis", style=T(bold=True))
    slide.update_style("default", T(size=20))
    slide.update_style("bold", T(size=22))

    lst = unordered_list(slide.box(p_top=20))
    lst.item().text("""~bold{Analysis of workflow schedulers in simulated distributed environments}
~emph{Jakub Beránek}, Stanislav Böhm, Vojtěch Cima
The Journal of Supercomputing 2022""")
    lst.item(p_top=10).text("""~bold{Runtime vs Scheduler: Analyzing Dask’s Overheads}
Stanislav Böhm, ~emph{Jakub Beránek}
IEEE/ACM Workflows in Support of Large-Scale Science (WORKS) 2020""")

    slide.box(p_top=40)
    slide.box(show="next+").text("(collaboration with ETH Zurich)", style=TextStyle(size=30))

    lst = unordered_list(slide.box(show="last+"))
    lst.item(p_top=20).text("""~bold{Network-Accelerated Non-Contiguous Memory Transfer}
S. Di Girolamo, K. Taranov, A. Kurth, M. Schaffner, T. Schneider, ~emph{J. Beránek}, M. Besta,
L. Benini, D. Roweth, T. Hoefler
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")
    lst.item(p_top=10).text("""~bold{A RISC-V in-Network Accelerator for Flexible High-Performance
Low-Power Packet Processing}
S. Di Girolamo, A. Kurth, A. Calotoiu, T. Benz, T. Schneider, ~emph{J. Beránek}, L. Benini, T. Hoefler
~emph{ISCA (International Symposium on Computer architecture) 2021}""")


@slides.slide()
def publications_unrelated(slide: Box):
    slide.box().text("Publications unrelated to thesis", style="bold")
    slide.update_style("default", T(size=16))
    slide.update_style("bold", T(size=20))

    slide.box(p_top=20).text("(collaboration with ETH Zurich)", style=T(size=26))

    lst = unordered_list(slide.box())
    lst.item(p_top=10).text("""~bold{SISA: Set-Centric Instruction Set Architecture for Graph Mining
on Processing-in-Memory System}
M. Besta, R. Kanakagiri, G. Kwasniewski, R. Ausavarungnirun, ~emph{J. Beránek}, K. Kanellopoulos,
K. Janda, Z. Vonarburg-Shmaria, L. Gianinazzi, I. Stefan, J. G. Luna, J. Golinowski, M. Copik,
L. Kapp-Schwoerer, S. Di Girolamo, N. Blach, M. Konieczny, O. Mutlu, T. Hoefler
~emph{IEEE/ACM MICRO (International Symposium on Microarchitecture) 2021}""")
    lst.item(p_top=10).text("""~bold{GraphMineSuite: Enabling High-Performance and Programmable
Graph Mining Algorithms with Set Algebra}
M. Besta, Z. Vonarburg-Shmaria, Y. Schaffner, L. Schwarz, G. Kwasniewski, L. Gianinazzi,
~emph{J. Beránek}, K. Janda, T. Holenstein, S. Leisinger, P. Tatkowski, E. Ozdemir, A. Balla,
M. Copik, P. Lindenberger, M. Konieczny, O. Mutlu, T. Hoefler
~emph{PVLDB 2021}""")
    lst.item(p_top=10).text("""~bold{Streaming Message Interface: High-Performance Distributed Memory
Programming on Reconfigurable Hardware}
T. De Matteis, J. de Fine Licht, ~emph{J. Beránek}, T. Hoefler
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")
    lst.item(p_top=40).text("""~bold{Haydi: Rapid Prototyping and Combinatorial Objects}
Stanislav Böhm, ~emph{Jakub Beránek}, Martin Šurkovský
~emph{Foundations of Information and Knowledge Systems 2018}""")
    lst.item(p_top=20).text("""~bold{Alternative Paths Reordering Using Probabilistic Time-Dependent
Routing}
M. Golasowski, ~emph{J. Beránek}, M. Šurkovský, L. Rapant, D. Szturcová, J. Martinovič, Kateřina Slaninová
~emph{Advances in Networked-based Information Systems 2020}""")
    lst.item(p_top=10).text("""~bold{A Distributed Environment for Traffic Navigation Systems}
J. Martinovič, M. Golasowski, K. Slaninová, ~emph{J. Beránek}, M. Šurkovský, L. Rapant, D. Szturcová, R. Cmar
~emph{Complex, Intelligent, and Software Intensive Systems 2020}""")


@slides.slide()
def outro(slide: Box):
    slide.box().text("Thank you for your attention", style=T(size=48))
    slide.box(p_top=300).text("Slides made with https://github.com/spirali/elsie", style=T(size=20))


@slides.slide()
def bonus_gromacs_workflow(slide: Box):
    content = slide_header_top(slide, "GROMACS + LiGEN LIGATE workflow")
    content.box(width="100%").image("images/gromacs-pipeline.png")


@slides.slide()
def bonus_projects(slide: Box):
    content = slide_header_top(slide, "Projects and publications")

    lst = unordered_list(content.box())
    lst.item().text("ANTAREX: distributed system for traffic simulator")
    lst.item().text("EVEREST: traffic simulator + HQ")
    lst.item().text("LIGATE: porting GROMACS + LiGEN workflow to HQ")
    lst.item().text("ETH internship: 5 publications (2 at SC'19)")


numbering_start = 2
numbering_end = 39


def page_numbering(slides: List[Box]):
    width = 90
    height = 45
    margin = 10

    for i, slide in enumerate(slides):
        if numbering_start <= (i + 1) <= numbering_end:
            box = slide.box(x=slide_width - width - margin,
                            y=slide_height - height - margin,
                            width=width,
                            height=height).rect(
                bg_color="#2F96A8", rx=5, ry=5
            )
            box.fbox(padding=5).text(f"{i + 1}/{numbering_end}",
                                     style=TextStyle(color="white", size=26, align="right"))


slides.render(slide_postprocessing=page_numbering)
# slides.render()
