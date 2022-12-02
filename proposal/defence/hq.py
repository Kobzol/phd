from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def hyperqueue(slides: Slides):
    @slides.slide()
    def hyperqueue(slide: Box):
        content = slide_header_top(slide, "HyperQueue")

        # HQ = team effort! main contributors => Ada Böhm & me
