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
from utils import slide_header_top, quotation
from workflows import workflows

WIDTH = 1600
HEIGHT = 900

slides = elsie.Slides(width=WIDTH, height=HEIGHT)
slides.update_style("default", T(font="Raleway", size=55, variant_numeric="lining-nums"))
slides.set_style("l2", T(size=34))
slides.set_style("bold", T(bold=True))
slides.set_style("emph", T(italic=True))
slides.set_style("header", T(size=60))


@slides.slide()
def intro(slide: Box):
    slide.box().text("""Ergonomics and efficiency
of workflows on HPC clusters""", style=T(size=60))
    slide.box(p_top=40).text("Jakub Beránek", T(size=46))

    style = T(align="left", size=34)
    supervisor = slide.box(x="5%", y="80%")
    supervisor.box(width=500).text("Supervisor", style=style)
    supervisor.box(width=500).text("Ing. Jan Martinovič, Ph.D.", style=style)

    slide.box(x="[95%]", y="80%", width=600).image("images/it4i-logo.png")


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
    content = slide_header_top(slide, "Thesis goal")
    content.box().text("""Design approches for executing workflows
on HPC clusters in an easy & efficient way""", T(size=54))

    # row = content.box(horizontal=True, p_top=100)
    # task_graph_1(row.box(show="next+"), size=75)
    # middle = row.box(width=50, height=50, p_left=75, p_right=75, show="next+")
    # middle.box().line((
    #     (middle.x(0).add(-40), middle.y("50%")),
    #     (middle.x("100%").add(40), middle.y("50%"))
    # ), end_arrow=Arrow(size=20), stroke_width=10)
    # cluster_box = row.box(show="last+")
    # cluster_1(cluster_box, size=75)


@slides.slide()
def objectives(slide: Box):
    content = slide_header_top(slide, "Thesis objectives")
    lst = ordered_list(content.box())
    lst.item(show="next+").text("Identify HPC workflow challenges")
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
    slide.box().text("Task graph challenges on HPC clusters", style=TextStyle(size=54))


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
def outro(slide: Box):
    slide.box().text("Thank you for your attention", style=T(size=60))
    slide.box(p_top=300).text("Slides made with https://github.com/spirali/elsie", style=T(size=40))


@slides.slide()
def questions_ismail_1(slide: Box):
    """
    1. The thesis identifies key challenges in task scheduling and resource management on heterogeneous
supercomputers. What are the most significant bottlenecks and how RSDS or HyperQueue addresses
these bottlenecks?
- Interaction with allocation managers, heterogeneous resource scheduling
- RSDS: speed-up of Dask
- HQ: integration of solutions in a single tool
    """
    slide = slide_header_top(slide, "Question 1 (prof. Ismail Hakki Toroslu)")

    quotation(slide.box(), """What are the most significant workflow bottlenecks and how
RSDS or HyperQueue addresses these bottlenecks?""", size=40)

    slide.update_style("default", T(size=50))
    lst = unordered_list(slide.box(p_top=40))
    lst.item(show="next+").text("Interaction with allocation managers")
    lst.item(show="next+").text("Heterogeneous resource management")
    lst.item(show="next+").text("Scalability")


@slides.slide()
def questions_ismail_2(slide: Box):
    """
    2. It is shown that simple scheduling heuristics like work-stealing can compete with more complex
algorithms. Under what conditions would a more complex algorithm be necessary?
- Specialized edge cases, e.g. memory consumption
    """
    slide = slide_header_top(slide, "Question 2 (prof. Ismail Hakki Toroslu)")

    quotation(slide.box(), """It is shown that simple scheduling heuristics like work-stealing
can compete with more complex algorithms. Under what conditions
would a more complex algorithm be necessary?""", size=40)

    slide.update_style("default", T(size=50))
    lst = unordered_list(slide.box(p_top=40))
    lst.item(show="next+").text("Specialized use-cases")
    lst.item(show="next+").text("Memory consumption limits")
    lst.item(show="next+").text("Latency (not throughput) optimized scheduling")


@slides.slide()
def questions_ismail_3(slide: Box):
    """
    3. Thesis mentions that Python runtime overhead is a critical bottleneck in Dask. How Rust-based
server (RSDS) reduces this overhead, and why Rust was chosen for this task over other languages?
- Compiled, memory layout, no GC, inlining
- Safer than C++ :)
    """
    slide = slide_header_top(slide, "Question 3 (prof. Ismail Hakki Toroslu)")

    quotation(slide.box(), """Thesis mentions that Python runtime overhead is a critical bottleneck in Dask.
How Rust-based server (RSDS) reduces this overhead, and why Rust was
chosen for this task over other languages?""", size=40)

    slide.update_style("default", T(size=50))
    lst = unordered_list(slide.box(p_top=40))
    lst.item(show="next+").text("Compiled to native code, small runtime, no GIL")
    lst.item(show="next+").text("Memory safety, data race safety")
    lst.item(show="next+").text("Compact task storage, binary message format")


@slides.slide()
def questions_ismail_4(slide: Box):
    """
    4. HyperQueue has already been adopted by several European supercomputing centers. Is there any
feedback that could be used to improve HyperQueue?
- Data transfers, Python API
    """
    slide = slide_header_top(slide, "Question 4 (prof. Ismail Hakki Toroslu)")

    quotation(slide.box(), """HyperQueue has already been adopted by several European supercomputing
centers. Is there any feedback that could be used to improve HyperQueue?""", size=40)

    slide.update_style("default", T(size=50))
    lst = unordered_list(slide.box(p_top=40))
    lst.item(show="next+").text("Missing features (data transfers, better Python API)")
    lst.item(show="next+").text("Better transparency of automatic allocation")


@slides.slide()
def questions_ismail_5(slide: Box):
    """
    5. Estee is designed to benchmark task schedulers and help prototype new algorithms. What future
extensions or improvements can be done on Estee, especially from HPC point of view?
- Support for more complex resource requirements
- Rewrite in Rust :)
    """
    slide = slide_header_top(slide, "Question 5 (prof. Ismail Hakki Toroslu)")

    quotation(slide.box(), """Estee is designed to benchmark task schedulers and help prototype
new algorithms. What future extensions or improvements can be done on Estee,
especially from HPC point of view?""", size=40)

    slide.update_style("default", T(size=50))
    lst = unordered_list(slide.box(p_top=40))
    lst.item(show="next+").text("Improve simulation throughput (Rust core + Python API)")
    lst.item(show="next+").text("Complex resource management")


@slides.slide()
def publications_related(slide: Box):
    slide = slide_header_top(slide, "Publications related to thesis")
    slide.update_style("default", T(size=30))
    slide.update_style("bold", T(size=32))

    margin = 40

    lst = unordered_list(slide.box(p_top=20))
    lst.item().text("""~bold{Analysis of workflow schedulers in simulated distributed environments}
~emph{Jakub Beránek}, Ada Böhm, Vojtěch Cima
The Journal of Supercomputing 2022""")
    lst.item(p_top=margin).text("""~bold{Runtime vs Scheduler: Analyzing Dask’s Overheads}
Ada Böhm, ~emph{Jakub Beránek}
IEEE/ACM Workflows in Support of Large-Scale Science (WORKS) 2020""")
    lst.item(p_top=margin).text("""~bold{HyperQueue: Efficient and ergonomic task graphs on HPC clusters}
~emph{Jakub Beránek}, Ada Böhm, Gianluca Palermo, Jan Martinovič, Branislav Jansík
SoftwareX 2024""")


@slides.slide()
def publications_unrelated(slide: Box):
    slide = slide_header_top(slide, "Publications unrelated to thesis")
    slide.update_style("default", T(size=16))
    slide.update_style("bold", T(size=20))

    margin = 40

    row = slide.box(horizontal=True)
    lst = unordered_list(row.box(), label=lambda a, b: "")
    lst.item(p_top=margin).text("""~bold{Network-Accelerated Non-Contiguous Memory Transfer}
S. Di Girolamo, K. Taranov, A. Kurth, M. Schaffner, T. Schneider, ~emph{J. Beránek}, M. Besta,
L. Benini, D. Roweth, T. Hoefler
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")
    lst.item(p_top=margin).text("""~bold{Streaming Message Interface: High-Performance Distributed Memory
Programming on Reconfigurable Hardware}
T. De Matteis, J. de Fine Licht, ~emph{J. Beránek}, T. Hoefler
~emph{SC (International Conference for High Performance Computing, Networking, Storage and Analysis) 2019}""")
    lst.item(p_top=margin).text("""~bold{A RISC-V in-Network Accelerator for Flexible High-Performance
Low-Power Packet Processing}
S. Di Girolamo, A. Kurth, A. Calotoiu, T. Benz, T. Schneider, ~emph{J. Beránek}, L. Benini, T. Hoefler
~emph{ISCA (International Symposium on Computer architecture) 2021}""")
    lst.item(p_top=margin).text("""~bold{SISA: Set-Centric Instruction Set Architecture for Graph Mining
on Processing-in-Memory System}
M. Besta, R. Kanakagiri, G. Kwasniewski, R. Ausavarungnirun, ~emph{J. Beránek}, K. Kanellopoulos,
K. Janda, Z. Vonarburg-Shmaria, L. Gianinazzi, I. Stefan, J. G. Luna, J. Golinowski, M. Copik,
L. Kapp-Schwoerer, S. Di Girolamo, N. Blach, M. Konieczny, O. Mutlu, T. Hoefler
~emph{IEEE/ACM MICRO (International Symposium on Microarchitecture) 2021}""")
    lst.item(p_top=margin).text("""~bold{GraphMineSuite: Enabling High-Performance and Programmable
Graph Mining Algorithms with Set Algebra}
M. Besta, Z. Vonarburg-Shmaria, Y. Schaffner, L. Schwarz, G. Kwasniewski, L. Gianinazzi,
~emph{J. Beránek}, K. Janda, T. Holenstein, S. Leisinger, P. Tatkowski, E. Ozdemir, A. Balla,
M. Copik, P. Lindenberger, M. Konieczny, O. Mutlu, T. Hoefler
~emph{PVLDB 2021}""")

    lst = unordered_list(row.box(y=0), label=lambda a, b: "")
    lst.item(p_top=margin).text("""~bold{Tunable and Portable Extreme-Scale Drug Discovery Platform at Exascale:
The LIGATE Approach}
G. Palermo, G. Accordi, D. Gadioli, E. Vitali, C. Silvano, B. Guindani, D. Ardagna, A. Beccari, D. Bonanni,
C. Talarico, F. Lughini, J. Martinovič, P. Silva, A. Böhm, ~emph{J. Beránek}, J. Křenek, B. Jansík, B. Cosenza,
L. Crisci, P. Thoman, P. Salzmann, T. Fahringer, L. Alexander, G. Tauriello, T. Schwede, J. Durairaj,
A. Emerson, F. Ficarelli, S. Wingbermühle, E. Lindahl, D. Gregori, E. Sana, S. Coletti, P. Gschwandtner
~emph{Proceedings of the 20th ACM International Conference on Computing Frontiers}""")
    lst.item(p_top=margin).text("""~bold{pyCaverDock: Python implementation of the popular tool for analysis
of ligand transport with advanced caching and batch calculation support}
O. Vávra, ~emph{J. Beránek}, J. Šťourač, M. Šurkovský, J. Filipovič, J. Damborský, J. Martinovič, D. Bednář
~emph{Bioinformatics 2023}""")
    lst.item(p_top=margin).text("""~bold{Haydi: Rapid Prototyping and Combinatorial Objects}
Stanislav Böhm, ~emph{Jakub Beránek}, Martin Šurkovský
~emph{Foundations of Information and Knowledge Systems 2018}""")
    lst.item(p_top=margin).text("""~bold{Alternative Paths Reordering Using Probabilistic Time-Dependent
Routing}
M. Golasowski, ~emph{J. Beránek}, M. Šurkovský, L. Rapant, D. Szturcová, J. Martinovič, Kateřina Slaninová
~emph{Advances in Networked-based Information Systems 2020}""")
    lst.item(p_top=margin).text("""~bold{A Distributed Environment for Traffic Navigation Systems}
J. Martinovič, M. Golasowski, K. Slaninová, ~emph{J. Beránek}, M. Šurkovský, L. Rapant, D. Szturcová, R. Cmar
~emph{Complex, Intelligent, and Software Intensive Systems 2020}""")


# @slides.slide()
# def bonus_projects(slide: Box):
#     content = slide_header_top(slide, "Projects and publications")
#
#     lst = unordered_list(content.box())
#     lst.item().text("ANTAREX: distributed system for traffic simulator")
#     lst.item().text("EVEREST: traffic simulator + HQ")
#     lst.item().text("LIGATE: porting GROMACS + LiGEN workflow to HQ")
#     lst.item().text("ETH internship: 5 publications (2 at SC'19)")


numbering_start = 2
numbering_end = 39


def page_numbering(slides: List[Box]):
    width = 90
    height = 45
    margin = 10

    for i, slide in enumerate(slides):
        if numbering_start <= (i + 1) <= numbering_end:
            box = slide.box(x=WIDTH - width - margin,
                            y=HEIGHT - height - margin,
                            width=width,
                            height=height).rect(
                bg_color="#2F96A8", rx=5, ry=5
            )
            box.fbox(padding=5).text(f"{i + 1}/{numbering_end}",
                                     style=TextStyle(color="white", size=26, align="right"))


# slides.render(slide_postprocessing=page_numbering)
slides.render()
