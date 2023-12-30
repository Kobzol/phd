import dataclasses
import datetime
import enum
from typing import List, Optional

import requests


# API: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers

@dataclasses.dataclass(frozen=True)
class Paper:
    bibname: str
    doi: Optional[str] = None
    arxiv: Optional[str] = None
    related: bool = False
    index: Optional[str] = None
    status: str = "published"
    impact_factor: Optional[float] = None
    SJR: Optional[float] = None

    def __post_init__(self):
        assert self.doi is not None or self.arxiv is not None

    def source(self) -> str:
        if self.arxiv is not None:
            return f"arxiv:{self.arxiv}"
        return self.doi


@dataclasses.dataclass(frozen=True)
class CitationAnalysis:
    paper: Paper
    own: List[str]
    nonown: List[str]
    venue: Optional[str] = None


def format_entry(analysis: CitationAnalysis) -> str:
    metadata = f"\\vspace{{2mm}}\\\\Status: {analysis.paper.status}\\\\"

    # Venue
    if analysis.venue is not None:
        if analysis.venue == "journal":
            venue = "journal"
            if analysis.paper.SJR is not None:
                venue += f" (SJR {analysis.paper.SJR})"
            elif analysis.paper.impact_factor is not None:
                venue += f" (IF {analysis.paper.impact_factor})"
            else:
                raise Exception(f"Journal paper without SJR or IF: {analysis}")
        elif analysis.venue == "conference":
            venue = "conference proceedings"
        else:
            assert False
        metadata += f"Type: {venue}\\\\"

    # Citations
    total_citations = len(analysis.own) + len(analysis.nonown)
    self_citations = len(analysis.own)
    if total_citations == 0:
        self_citation_text = ""
    elif self_citations == 0:
        self_citation_text = " (no self citations)"
    elif self_citations == 1:
        self_citation_text = " (1 self citation)"
    else:
        self_citation_text = f" ({self_citations} self citations)"
    metadata += f"""Total citations: {total_citations}{self_citation_text}\\\\"""

    # Index
    if analysis.paper.index is not None:
        metadata += f"Index: {analysis.paper.index}"

    return f"\t\t\\item\\fullcite{{{analysis.paper.bibname}}}{metadata}\n"


if __name__ == "__main__":
    papers: List[Paper] = [
        Paper(bibname="rsds", doi="10.1109/WORKS51914.2020.00006", related=True, index="SCOPUS"),
        Paper(bibname="estee", doi="10.1007/s11227-022-04438-y", related=True, index="SCOPUS", SJR=0.684),
        Paper(bibname="ligate", doi="10.1145/3587135.3592172", related=True, index="SCOPUS"),
        Paper(bibname="sisa", doi="10.1145/3466752.3480133", index="SCOPUS"),
        Paper(bibname="graphminesuite", doi="10.14778/3476249.3476252", index="SCOPUS", SJR=2.376),
        Paper(bibname="spin", doi="10.1145/3295500.3356189", index="SCOPUS"),
        Paper(bibname="spin2", doi="10.1109/ISCA52012.2021.00079", index="SCOPUS"),
        Paper(bibname="pspin", arxiv="2010.03536"),
        Paper(bibname="smi", doi="10.1145/3295500.3356201", index="SCOPUS"),
        Paper(bibname="haydi", doi="10.1007/978-3-319-90050-6\\_8", index="SCOPUS"),
        Paper(bibname="pycaverdock", doi="10.1093/bioinformatics/btad443", index="SCOPUS", impact_factor=5.8),
        Paper(bibname="traffic_simulator_1", doi="10.1007/978-3-030-29029-0_22", index="SCOPUS"),
        Paper(bibname="traffic_simulator_2", doi="10.1007/978-3-030-22354-0_27", index="SCOPUS"),
    ]

    sources = [p.source() for p in papers]
    response = requests.post(
        f"https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,authors,publicationVenue,citations,citations.title,citations.authors",
        json={
            "ids": sources
        }).json()
    if isinstance(response, dict) and response.get("code") == "429":
        raise Exception("Too many requests")

    analysed = []
    for (paper, data) in zip(papers, response):
        title = data["title"]
        authors = data["authors"]
        paper_author_ids = set(author["authorId"] for author in authors)

        own_citations = []
        nonown_citations = []
        for citation in data["citations"]:
            citation_author_ids = set(author["authorId"] for author in citation["authors"])
            nonown = paper_author_ids.isdisjoint(citation_author_ids)
            if nonown:
                nonown_citations.append(citation["title"])
            else:
                own_citations.append(citation["title"])

        print(title)
        print(f"Own citations: {len(own_citations)}")
        print(f"Non-own citations: {len(nonown_citations)}")
        print(f"Total citations: {len(own_citations) + len(nonown_citations)}")
        print()

        venue_data = data["publicationVenue"]
        venue = venue_data.get("type")
        analysed.append(CitationAnalysis(paper=paper, own=own_citations, nonown=nonown_citations, venue=venue))

    related = [analysis for analysis in analysed if analysis.paper.related and analysis.venue is not None]
    nonrelated = [analysis for analysis in analysed if not analysis.paper.related and analysis.venue is not None]

    now = datetime.datetime.now()
    date_formatted = now.strftime("%d. %m. %Y")
    with open("chapters/publications-generated.tex", "w") as f:
        f.write(f"""Citation data was taken from Semantic Scholar\\footnoteurl{{https://semanticscholar.org}} on {date_formatted}.
Self citation is defined as a citation by a publication where at least a single author is also the
author of the cited paper. SJR (Scientific Journal Rankings) ranking was taken from Scimago Journal\\footnoteurl{{https://www.scimagojr.com}},
IF (Impact Factor) ranking was taken from Oxford Academic\\footnoteurl{{https://academic.oup.com/bioinformatics}}.

Note that Ada Böhm was named Stanislav Böhm in older publications.
""")

        f.write("""
\\section*{Publications Related to Thesis}
    \\begin{itemize}
""")
        for item in related:
            f.write(format_entry(item))
        f.write("\\end{itemize}\n")

        f.write("""
\\newpage
\\section*{Publications Not Related to Thesis}
    \\begin{itemize}
""")
        for item in nonrelated:
            f.write(format_entry(item))
        f.write("\\end{itemize}\n")
