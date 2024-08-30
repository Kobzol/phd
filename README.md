# PhD thesis
This repository contains source code and the final version of my PhD thesis titled `Ergonomics and efficiency of workflows on HPC clusters`.

You can find the rendered thesis [here](output/thesis.pdf).

The goal of my thesis was to design approaches that would enable the effortless and efficient execution of task graphs (DAGs, workflows, pipelines, …) on heterogeneous HPC (High-Performance Computing) clusters, aka supercomputers. This research led to the following three main outputs/contributions:

- [HyperQueue](https://github.com/it4innovations/hyperqueue)
  - HyperQueue is an HPC-focused task runtime that can automatically load balance task graphs across different Slurm/PBS allocations and provides sophisticated heterogeneous resource management.
  - It is actively being used by researchers in various HPC centers across Europe; I consider it to be the most successful output of my thesis.
  - You can find more about it in [HyperQueue: Efficient and ergonomic task graphs on HPC clusters](
    https://www.softxjournal.com/article/S2352-7110(24)00185-7/fulltext) and in Chapter 7 of my [thesis](output/thesis.pdf).
- [RSDS](https://github.com/it4innovations/rsds)
  - RSDS is a reimplementation of the [Dask](https://www.dask.org/) server and scheduler, which improves its performance in HPC scenarios and is backwards compatible with existing Dask programs.
  - We have analyzed the overheads of Dask and evaluated RSDS's design and performance in [Runtime vs Scheduler: Analyzing Dask’s Overheads](https://www.computer.org/csdl/proceedings-article/works/2020/104000a001/1q7jxiyDsFW).
- [Estee](https://github.com/it4innovations/estee)
  - Estee is a Python task graph execution simulator that can be used to prototype task scheduling algorithms.
  - We have used it to perform a study of several scheduling algorithms in [Analysis of workflow schedulers in simulated distributed environments](https://link.springer.com/article/10.1007/s11227-022-04438-y).
