from typing import List, Optional, Tuple

import elsie
from elsie import Arrow, SlideDeck
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.slides.slide import Slide
from elsie.text.textstyle import TextStyle, TextStyle as T

from challenges import challenges
from estee import estee
from hq import hyperqueue
from rsds import rsds
from sota import sota
from questions import questions
from tasks import cluster_1, task_graph_1
from utils import slide_header_top
from workflows import workflows

PRODUCTION_BUILD = False

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


@slides.slide()
def goal(slide: Box):
    content = slide_header_top(slide, "Thesis goal")
    content.box().text("""Design approches for executing workflows
on HPC clusters in an easy & efficient way""", T(size=54))

    row = content.box(horizontal=True, p_top=100)
    task_graph_1(row.box(show="next+"), size=75)
    middle = row.box(width=50, height=50, p_left=75, p_right=75, show="next+")
    middle.box().line((
        (middle.x(0).add(-40), middle.y("50%")),
        (middle.x("100%").add(40), middle.y("50%"))
    ), end_arrow=Arrow(size=20), stroke_width=10)
    cluster_box = row.box(show="last+")
    cluster_1(cluster_box, size=75)


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
    content.box().text(text, style=T(size=60))


topic_highlight(slides, """Ergonomics and efficiency
of ~highlight{workflows on HPC clusters}""")

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


@slides.slide()
def outro(slide: Box):
    slide.box().text("Thank you for your attention", style=T(size=60))
    slide.box(p_top=300).text("Slides made with https://github.com/spirali/elsie", style=T(size=40))


questions(slides)

def ferris(slides: SlideDeck):
    count = sum(slide.steps() for slide in slides._slides)

    def calculate_dim(slide: Slide, progress: float) -> Tuple[float, Tuple[float, float]]:
        size = 80
        if slide.view_box is not None:
            size *= slide.view_box[2] / WIDTH

            reference_x = slide.view_box[2] + slide.view_box[0]

            x_first = reference_x
            x_last = reference_x - (size * 1.05)
            x_diff = abs(x_first - x_last)
            x = x_first - progress * x_diff
        else:
            x_first = WIDTH
            x_last = WIDTH - (size * 1.05)
            x_diff = abs(x_first - x_last)
            x = x_first - progress * x_diff

        if slide.view_box is not None:
            y = int(HEIGHT * 0.02)
            y += slide.view_box[1] + 32
        else:
            y = int(HEIGHT * 0.02)

        return (size, (x, y))

    total_steps = 0
    for i, slide in enumerate(slides._slides):
        steps = slide.steps()
        for step in range(steps):
            progress = (total_steps + step) / count
            (size, (x, y)) = calculate_dim(slide, progress=progress)
            slide.box().box(show=step + 1, x=x, y=y, width=size, height=size).image(
                "images/ferris.svg")
        total_steps += steps

numbering_start = 2
numbering_end = 39


def page_numbering(slides: List[Box]):
    width = 70
    height = 70
    margin = 5

    for i, slide in enumerate(slides):
        if numbering_start <= (i + 1) <= numbering_end:
            box = slide.box(x=WIDTH - width - margin,
                            y=HEIGHT - height - margin,
                            width=width,
                            height=height).rect(
                bg_color="#2F96A8", rx=10, ry=10
            )
            box.fbox(padding=5).text(f"{i + 1}",
                                     style=TextStyle(color="white", size=36))


# ferris(slides)

if PRODUCTION_BUILD:
    slides.render(slide_postprocessing=page_numbering)
else:
    slides.render()
