from elsie import Slides, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import slide_header_top


def hpc_overview(slides: Slides):
    @slides.slide()
    def hpc(slide: Box):
        content = slide_header_top(slide, "HPC (High-Performance Computing)")

        lst = unordered_list(content.box())
        lst.item().text("Crucial for scientific advancements")
        lst.item(show="next+").text("Enables the most complex experiments")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Complex system modelling", style="l2")
        lst2.item(show="next+").text("Material simulations", style="l2")
        lst2.item(show="next+").text("Machine learning", style="l2")
        lst.item(show="next+").text("Complex hardware + software stack")

    @slides.slide()
    def hpc_hw(slide: Box):
        content = slide_header_top(slide, "HPC hardware (clusters)")

        lst = unordered_list(content.box())
        lst.item().text("Large number of powerful nodes")
        lst2 = lst.ul()
        lst2.item().text("Hundreds/thousands nodes per cluster", style="l2")
        lst2.item().text("64-128 CPU cores per node", style="l2")
        lst.item(show="next+").text("Heterogeneous nodes")
        lst2 = lst.ul()
        lst2.item().text("GPUs, FPGAs, TPUs, …", style="l2")
        lst2.item().text("Complex memory hierarchy (NUMA)", style="l2")
        lst.item(show="next+").text("Very fast network")
        lst2 = lst.ul()
        lst2.item().text("Up to 400 Gb/s", style="l2")

    @slides.slide()
    def hpc_sw(slide: Box):
        content = slide_header_top(slide, "HPC software")

        tech = TextStyle(size=24)
        lst = unordered_list(content.box())
        lst.item().text("Many technologies and frameworks")
        lst2 = lst.ul()
        lst2.item(show="next+").text(
            "MPI, RDMA, CUDA, HIP, OpenMP, OpenACC, OpenCL, SYCL, oneAPI, HLS, AVX, BLAS, …",
            style=tech)
        lst2.item(show="next+").text("numpy, pandas, cupy, TensorFlow, PyTorch, JAX, …",
                                     style=tech)
        lst2.item(show="next+").text("C, C++, Fortran, Python, …", style=tech)
        lst.item(show="next+").text("Optimizing HPC apps => full-time job")
        lst2 = lst.ul()
        lst2.item(show="next+").text("Time-consuming and challenging for scientists", style="l2")
