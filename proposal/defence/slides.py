import elsie
from elsie import Arrow
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.text.textstyle import TextStyle as T

from challenges import challenges
from estee import estee
from hpc import hpc_overview
from hq import hyperqueue
from rsds import rsds
from sota import sota
from tasks import cluster_1, task_graph_1
from utils import slide_header_top
from workflows import workflows

slides = elsie.Slides()
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
    supervisor.box(width=400).text("Ing. Jan Martinovič Ph.D.", style=style.compose(T(bold=True)))

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
of workflows on HPC clusters""")
    content.box().text("Goal", style="bold")
    content.box().text("""Help users to execute complex task workflows
on HPC clusters in an easy & scalable way""")

    row = content.box(horizontal=True, p_top=40)
    task_graph_1(row.box(show="next+"), size=75)
    middle = row.box(width=50, height=50, p_left=75, p_right=75, show="next+")
    middle.box().line((
        (middle.x(0).add(-40), middle.y("50%")),
        (middle.x("100%").add(40), middle.y("50%"))
    ), end_arrow=Arrow(), stroke_width=4)
    cluster_box = row.box(show="last+")
    cluster_1(cluster_box, size=75)


def topic_highlight(slides: elsie.Slides, text: str):
    slide = slides.new_slide()
    slide.set_style("highlight", T(bold=True))
    slide.box().text(text, style=T(size=48))


topic_highlight(slides, """Ergonomics and efficiency
of workflows on ~highlight{HPC clusters}""")

hpc_overview(slides)

topic_highlight(slides, """Ergonomics and efficiency
of ~highlight{workflows} on HPC clusters""")

workflows(slides)

topic_highlight(slides, """~highlight{Ergonomics and efficiency}
of workflows on HPC clusters""")

challenges(slides)
sota(slides)


@slides.slide()
def objectives(slide: Box):
    content = slide_header_top(slide, "Objectives")
    lst = ordered_list(content.box())
    lst.item(show="next+").text("Identify HPC workflow challenges")
    lst.item(show="next+").text("Design improvements")
    lst.item(show="next+").text("Implement them in a task runtime")


hyperqueue(slides)
estee(slides)
rsds(slides)


@slides.slide()
def recap(slide: Box):
    content = slide_header_top(slide, "Recap: workflows on HPC")

    lst = unordered_list(content.box())
    lst.item().text("Ergonomics", style="bold")
    lst2 = lst.ul()
    lst2.item().text("Bypass job manager", style="l2")
    lst2.item().text("Fine-grained resource requirements", style="l2")
    lst.item(show="next+").text("Efficiency", style="bold")
    lst2 = lst.ul()
    lst2.item().text("Minimize runtime overhead", style="l2")


@slides.slide()
def next_steps(slide: Box):
    content = slide_header_top(slide, "Next steps")

    lst = unordered_list(content.box())
    lst.item().text("HyperQueue performance study")
    lst2 = lst.ul()
    lst2.item().text("Compare with other task runtimes", style="l2")
    lst.item(show="next+").text("Analysis of auto-allocation")
    lst2 = lst.ul()
    lst2.item().text("Compare allocation strategies", style="l2")
    lst2.item().text("Analyze efficiency", style="l2")


@slides.slide()
def publications_related(slide: Box):
    slide.box().text("Publications related to thesis", style=T(bold=True))

    box = slide.box(p_top=20)
    box.update_style("default", T(size=20))
    box.update_style("bold", T(size=22))

    lst = unordered_list(box)
    lst.item().text("""~bold{Analysis of workflow schedulers in simulated distributed environments}
~emph{Jakub Beránek}, Stanislav Böhm, Vojtěch Cima
The Journal of Supercomputing 2022""")
    lst.item(p_top=10).text("""~bold{Runtime vs Scheduler: Analyzing Dask’s Overheads}
Stanislav Böhm, ~emph{Jakub Beránek}
IEEE/ACM Workflows in Support of Large-Scale Science (WORKS) 2020""")


@slides.slide()
def publications_unrelated_eth(slide: Box):
    slide.box().text("Publications unrelated to thesis", style="bold")
    slide.box().text("(collaboration with ETH Zurich)", style=T(size=26))

    box = slide.box(p_top=20)
    box.update_style("default", T(size=20))
    box.update_style("bold", T(size=22))
    box.set_style("small", T())

    lst = unordered_list(box)
    lst.item().text("""~bold{A RISC-V in-Network Accelerator for Flexible High-Performance
Low-Power Packet Processing}
~small{S. Di Girolamo, A. Kurth, A. Calotoiu, T. Benz, T. Schneider, ~emph{J. Beránek}, L. Benini, T. Hoefler}
~emph{ISCA (International Symposium on Computer architecture) 2021}""")
    lst.item(p_top=20).text("""~bold{SISA: Set-Centric Instruction Set Architecture for Graph Mining
on Processing-in-Memory System}
~small{M. Besta, R. Kanakagiri, G. Kwasniewski, R. Ausavarungnirun, ~emph{J. Beránek}, K. Kanellopoulos,
K. Janda, Z. Vonarburg-Shmaria, L. Gianinazzi, I. Stefan, J. G. Luna, J. Golinowski, M. Copik,
L. Kapp-Schwoerer, S. Di Girolamo, N. Blach, M. Konieczny, O. Mutlu, T. Hoefler}
~emph{IEEE/ACM MICRO (International Symposium on Microarchitecture) 2021}""")
    lst.item(p_top=10).text("""~bold{GraphMineSuite: Enabling High-Performance and Programmable
Graph Mining Algorithms with Set Algebra}
~small{M. Besta, Z. Vonarburg-Shmaria, Y. Schaffner, L. Schwarz, G. Kwasniewski, L. Gianinazzi,
~emph{J. Beránek}, K. Janda, T. Holenstein, S. Leisinger, P. Tatkowski, E. Ozdemir, A. Balla,
M. Copik, P. Lindenberger, M. Konieczny, O. Mutlu, T. Hoefler}
~emph{PVLDB 2021}""")
    lst.item(p_top=10).text("""~bold{Network-Accelerated Non-Contiguous Memory Transfer}
~small{S. Di Girolamo, K. Taranov, A. Kurth, M. Schaffner, T. Schneider, ~emph{J. Beránek}, M. Besta,
L. Benini, D. Roweth, T. Hoefler}
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")
    lst.item(p_top=10).text("""~bold{Streaming Message Interface: High-Performance Distributed Memory
Programming on Reconfigurable Hardware}
T. De Matteis, J. de Fine Licht, ~emph{J. Beránek}, T. Hoefler
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")


@slides.slide()
def publications_unrelated_other(slide: Box):
    slide.box().text("Publications unrelated to thesis", style="bold")

    box = slide.box(p_top=20)
    box.update_style("default", T(size=20))
    box.update_style("bold", T(size=22))

    lst = unordered_list(box)
    lst.item().text("""~bold{Haydi: Rapid Prototyping and Combinatorial Objects}
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


slides.render()
