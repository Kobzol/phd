from collections import defaultdict
from typing import List

from attr import dataclass
from elsie import SlideDeck
from elsie.ext import unordered_list
from elsie import TextStyle as T

from utils import quotation, slide_header_top


@dataclass
class Question:
    question: str
    answers: List[str]
    author: str


def questions(slides: SlideDeck):
    Q = Question
    jura = "doc. Mgr. Jiří Dvorský, Ph.D."
    ismail = "prof. Ismail Hakki Toroslu"
    joao = "assoc. prof. João Manuel Paiva Cardoso"
    questions = [
        # As a hardware resource, yes, but HQ won't run on a quantum computer
        Q("""Will it be possible to apply HyperQueue to a quantum computer as well?""", [], jura),
        Q("""The thesis identifies key challenges in task scheduling and resource management
on heterogeneous supercomputers. What are the most significant bottlenecks
and how RSDS or HyperQueue addresses these bottlenecks?""", [
            "RSDS: runtime optimization, scalability",
            "HQ: interaction with allocation managers",
            "HQ: heterogeneous resource management",
        ], ismail),
        Q("""It is shown that simple scheduling heuristics like work-stealing
can compete with more complex algorithms. Under what conditions
would a more complex algorithm be necessary?""", [
            "Specialized use-cases",
            "Memory consumption limits",
            "Latency (not throughput) optimized scheduling"
        ], ismail),
        Q("""Thesis mentions that Python runtime overhead is a critical bottleneck in Dask.
How Rust-based server (RSDS) reduces this overhead, and why Rust was
chosen for this task over other languages?""", [
            "Compact task storage, better message format",
            "Compiled to native code, small runtime, no GIL",
            "Memory safety, data race safety",
        ], ismail),
        Q("""HyperQueue has already been adopted by several European supercomputing
centers. Is there any feedback that could be used to improve HyperQueue?""", [
            "Missing features (data transfers, better Python API)",
            "Better transparency of automatic allocation"
        ], ismail),
        Q("""Estee is designed to benchmark task schedulers and help prototype
new algorithms. What future extensions or improvements can be done on Estee,
especially from HPC point of view?""", [
            "Improve simulation throughput (e.g. Rust core + Python API)",
            "Heterogeneous resource management"
        ], ismail),
        Q("""Does the support of only acyclic task graphs may impose less efficient solutions
in cases where loops involved regions of tasks? What kind of advantages
and disadvantages do you see in using acyclic task graphs? Do the iterative task
graphs transformed into acyclic task graphs (such as L-DAG), or each iteration
as a separate task, fully solve the problem without disadvantages?""", [
            "Static loop count => unrolling", # overhead
            "Dynamic loop count => dynamic tasks",
            "Iterations complicate the programming model"
        ], joao),
        Q("""Based on your experience, is there a list of recommendations to guide
developers/users w.r.t. task granularity? Is the control of the task graph granularity,
based on the invocation of functions (e.g., in Python), a good approach?""", [
            "More granularity => better load balancing, more overhead",
            "Task runtimes should adopt to the granularity required by its users",
        ], joao),
        Q("""What are the implications of not considering pipelining execution of tasks?
How could this restriction be solved?""", [
            "Complicates task completion semantics",
            "Potential future work for HyperQueue",
        ], joao),
        Q("""How does DASK support symbolic task graph representations? Should they
need to be rematerialized, or can the runtime system directly use the
symbolic representation to schedule and instantiate them?""", [
            "Task graphs are rematerialized on the Dask server",
            "Incremental rematerialization",
            "Experimental research: represent task graphs with finite automata",
        ], joao),
        Q("""How does the information for each task input into the runtime system,
e.g., the number of nodes needed? Is the information in the form of annotations?
Is it in the task graph representation?""", [
            "Dependency/resource information is embedded in the DAG",
            "Configuration depends on the interface (Python, CLI, TOML)",
            "HQ uses structural sharing for shared requirements"
        ], joao),
        Q("""What kind of fault-tolerance schemes are included?
How can other fault-tolerance schemes be included?""", [
            "Tasks are resilient to worker failures (task instances)",
            "Tasks are resilient to server failures (journaling)",
            "Potential future work: task checkpointing"
        ], joao),
        Q("""The example in Fig. 3.2 seems to not consider the different execution time of
tasks according to the worker. When there are differences, for instance because of the use
of different computing units (CPU vs GPU), how does the scheduling decide?""", [
            # TODO
        ], joao),
        Q("""What kind of possibilities do you see if we also consider variants of the tasks, using the same CPU,
but with different energy/execution time trade-offs?""", [
            # TODO
        ], joao),
        Q("""The use of checkpointing, although convenient, usually introduces a large
overhead. Is this overhead automatically managed or it needs to be
explicitly managed by the user?""", [
            "HQ optionally stores a (GZIP-compressed) event journal on disk"
        ], joao),
        Q("""The ESTEE architecture shown in Fig. 5.1 in unclear in terms of some of the inputs
to the framework. E.g., allocated resources, target clustering configuration, etc.
Could you explain in more detail how the inputs are described and what kind of
inputs are expected? Also, in listing 5.1 there is no mention of target cluster, #CPUs,
connections, etc. Could you explain more about how that information is input?
Could you explain about the ESTEE simple “communication network model”.""", [
            # TODO
        ], joao),
        Q("""In terms of the scheduler, does the runtime system use updated
execution times measured at runtime? And if so, how does it deal with that?""", [
            "ESTEE does not do that, it is emulated by the ~emph{mean} imode",
            "Users decide task durations, so measuring them is not so important"
        ], joao),
        Q("""Do the schedulers and the evaluation in subsection 5.2 deal with
goals to use fewer CPUs as much as possible (part of the work selection strategy)?
If so, how does it work?""", [
            # TODO
        ], joao),
        Q("""When considering different task graphs and the impact of them on the gap
between the two network models in subsection 5.2, do you think that
understanding the shape and main characteristics of the task graphs would help
to improve scheduling decisions?""", [
            "Heuristics"
            # TODO
        ], joao),
        Q("""Trends in terms of scheduler performance relative to b-level (in DASK and ESTEE,
page 75) with different cluster configurations? Any thoughts about the effect
of the task graph shapes/patterns on the accuracy of relative performance?""", [
            "Runtime overhead, network noise, ... have a large effect"
        ], joao),
        Q("""Any task graph pattern/shape would be able to indicate when a scheduler
is better than others and thus could be the one used? Use of the best for
a particular task graph and cluster configuration.""", [
            "Graph shape can be a heuristic for selecting a scheduler"
        ], joao),
        Q("""Any thoughts based on the experiments about the MSD (minimal scheduling delay)
impact according to the scheduler and task graph? Long MSD implies less
decisions of the scheduler but more knowledge (arrival of more task events).
Does MSD imply similar effects on different information modes?""", [
            # TODO
        ], joao),
        Q("""The task runtime optimization evaluations would benefit from the knowledge of
optimal scheduling. This could be very important to understand the potential
for further improvements in terms of the actual results with heuristics.
Do you see an experimental way to know those optimal results?""", [
            "Complex benchmarks generated from real-world numpy/pandas code",
            "NP-hard"
        ], joao),
        Q("""The limitation of tasks in pure Python and on the constraint to workers behave
in a single-threaded fashion, which was solved by executing multiple instances
on the same node, and running in a separate process, and thus each worker using
a copy of a CPython interpreter and a copy of GIL, may have a high overhead. Any
thoughts on that overhead and when it is adequate to circumvent the limitation?""", [
            "Each worker introduces scheduling and communication overhead",
            "Python 3.13+ has support for running without GIL"
        ], joao),
        Q("""Any thoughts about the main conclusions regarding I/O-bound
vs computer-bound benchmarks?""", [
            "Compute-bound vs I/O-bound makes a large difference",
            "'Time spent in Python' vs 'Time spent in C/C++ or I/O or other program'",
        ], joao),
        Q("""Fig. 6.2 and 6.3 (page 86) show the overhead per task when increasing the number
of tasks and using two benchmarks (“merge” and “merge-25000”). Are the results
similar to other benchmarks? Why the use of these benchmarks and the ones in
Fig. 6.4 and 6.5 (page 87) for studying the scaling of DASK and the effect of GIL?""", [
            # TODO
        ], joao),
        Q("""The manual tuning of worker configuration (impact of worker per core and the
non-optimal scalability of DASK) for some workflows seems very important
to improve performance. Any idea if this can be statically determined?""", [
            "Very difficult to determine, can differ task by task"
        ], joao),
        Q("""Any thoughts about providing schedulers the worker network connections?
Do you see a relevant impact on RSDS?""", [], joao),
        Q("""Since RSDS does not implement all DASK message types, do you see in
future plans their integration to RSDS, or are there technical challenges
that do not justify their integration?""", [
            "Some messages are Python specific",
            "'Run this Python code on the server'"
            # We could spawn CPython on the server
        ], joao),
        Q("""Why do the schedulers (ws and random) integrated in RSDS do not
include a list-scheduling or an ALAP scheduling scheme?""", [
            "Work-stealing is list scheduling (B-level) + balancing between workers",
            "We focused on runtime optimization"
        ], joao),
        Q("""The conclusion that the improved performance of RSDS with ws is caused by
better runtime efficiency and not by better schedules seems to result from the
large overhead of the DASK implementation. (page 93)
Could you comment on this?""", [
            "RSDS/ws vs Dask/ws: 1.66x",
            "Dask/random vs Dask/ws: 0.95x",
            "RSDS/random vs Dask/ws: 1.41x"
        ], joao),
        Q("""The results presented in Fig. 6.11, page 96, seem to indicate a greater dependence
of DASK to #workers (its “performance is reduced significantly with each
additional worker”) than RSDS. Could you elaborate on that? Could part of
the overhead reduction of RSDS over DASK, besides the implementation used,
be because of the much simpler ws scheduling scheme used by RSDS when
compared to DASK?""", [
            "Important to avoid O(workers^2) algorithms",
            "Dask is more penalized for worker I/O"
        ], joao),
        Q("""Do the overheads of DASK and RSDS for each task depend on the number
of workers and tasks in the task graph? What is the reason for the significant
overhead increase in RSDS with some of the benchmarks (Fig. 6.14, page 98)?""", [
            # TODO
        ], joao),
        Q("""The thesis mentions that task graphs are represented in a compressed
format, but that format is not sully described. Could you elaborate on this?""", [
            "Representation of a task x number of tasks",
            "Currently used only for task arrays (DAGs without dependencies)",
            "Could be extended to support also task dependencies (Dask does this)"
        ], joao),
        Q("""Why the fractional resource requirements in HYPERQUEUE are not defined
as integer percentages and need to use fixed-point representations?""", [
            "Fixed-point arithmetic is essentially integer percentages",
            "Floating point operations have precision problems"
        ], joao),
        Q("""It is interesting that HYPERQUEUE showed unnecessary tuning on the
number of used nodes and workers, and number of tasks and task durations,
as opposite of DASK has shown. What is the main reason for this?""", [
            "No GIL",
            "Single node = single worker, which manages all node resources",
        ], joao),
        Q("""How do you see the possible support of HYPERQUEUE to data transfers
directly between tasks? And to streaming and task pipelining support?""", [
            "This is currently in-progress",
            "Need to figure out task completion semantics"
        ], joao)
    ]

    render_questions(slides, questions)


def render_questions(slides: SlideDeck, questions: List[Question]):
    # question_counts = defaultdict(int)
    # for question in questions:
    #     question_counts[question.author] += 1
    #
    # question_counts = sorted(question_counts.items(), key=lambda v: v[1])
    #
    # slide = slides.new_slide()
    # slide = slide_header_top(slide, "Reviewer questions")
    # lst = unordered_list(slide.box())
    # for (author, count) in question_counts:
    #     lst.item().text(f"{author}: {count} question{'' if count == 1 else 's'}")

    last_author = None
    counter = 0
    for question in questions:
        if question.author != last_author and last_author is not None:
            counter = 0

        slide = slides.new_slide()
        slide = slide_header_top(slide, f"Question {counter + 1} ({question.author})")

        quotation(slide.box(), question.question, size=40)

        slide.update_style("default", T(size=46))
        lst = unordered_list(slide.box(p_top=40))
        for answer in question.answers:
            lst.item(show="next+").text(answer)

        counter += 1
        last_author = question.author
