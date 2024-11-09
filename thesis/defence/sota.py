from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def sota(slides: Slides):
    @slides.slide()
    def task_duration(slide: Box):
        content = slide_header_top(slide, "State of the art: task duration")
        content.box(width="70%", p_top=40).image("images/sota.svg")

    @slides.slide()
    def task_duration(slide: Box):
        content = slide_header_top(slide, "State of the art: allocation manager")
        content.box(width="60%").image("images/sota-pbs.svg")

    @slides.slide()
    def other(slide: Box):
        content = slide_header_top(slide, "State of the art: resources & multi-node")
        lst = unordered_list(content.box())
        lst.item().text("Resource requirements: usually simplistic")
        lst.item(show="next+").text("Multi-node tasks: separate concept")
