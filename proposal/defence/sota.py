from elsie import Slides
from elsie.boxtree.box import Box

from utils import slide_header_top


def sota(slides: Slides):
    @slides.slide()
    def sota_1(slide: Box):
        content = slide_header_top(slide, "SOTA")
        # TODO
