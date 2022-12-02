from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def challenges(slides: Slides):
    @slides.slide()
    def workflows_definition(slide: Box):
        content = slide_header_top(slide, "Task-based workflows")

        lst = unordered_list(content.box())
        lst.item(label="=").text("pipelines, workflows, task graphs, …")
        lst.item(show="next+").text("Popular programming model")
