import dataclasses
import datetime
import os
from typing import List, Optional

import pybliometrics.scopus.exception
import requests
import tqdm

# Scopus API key
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")


# Scopus: https://www.scopus.com/hirsch/author.uri?accessor=authorProfile&auidList=57202037909&origin=AuthorProfile&display=hIndex
# SemanticScholar API: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers

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


@dataclasses.dataclass(frozen=True)
class CitationAnalysis:
    paper: Paper
    own: List[str]
    nonown: List[str]
    year: int
    journal: Optional[bool] = None


def format_entry(analysis: CitationAnalysis) -> str:
    metadata = "\\par{}"
    # metadata += f"Status: {analysis.paper.status} ({analysis.year})\\\\"

    # Citations
    total_citations = len(analysis.own) + len(analysis.nonown)
    self_citations = len(analysis.own)
    if total_citations == 0:
        self_citation_text = ""
    elif self_citations == 0:
        self_citation_text = " (no self-citations)"
    elif self_citations == 1:
        self_citation_text = " (1 self-citation)"
    else:
        self_citation_text = f" ({self_citations} self-citations)"
    metadata += f"""Total citations: {total_citations}{self_citation_text}"""

    # Venue
    if analysis.journal is not None:
        if analysis.journal:
            venue = "journal"
            if analysis.paper.SJR is not None:
                venue += f" (SJR {analysis.paper.SJR})"
            elif analysis.paper.impact_factor is not None:
                venue += f" (IF {analysis.paper.impact_factor})"
            else:
                raise Exception(f"Journal paper without SJR or IF: {analysis}")
        else:
            venue = "conference proceedings"
        metadata += f", venue: {venue}"

    # Index
    # if analysis.paper.index is not None:
    #     metadata += f"Index: {analysis.paper.index}"

    return f"\t\t\\item\\fullcite{{{analysis.paper.bibname}}}{metadata}\n"


class SemanticScholarResolver:
    def name(self) -> str:
        return "Semantic Scholar"

    def url(self) -> str:
        return "https://www.semanticscholar.org"

    def resolve(self, papers: List[Paper]) -> List[CitationAnalysis]:
        def source(paper: Paper) -> str:
            if paper.arxiv is not None:
                return f"arxiv:{paper.arxiv}"
            return paper.doi

        sources = [source(p) for p in papers]
        response = requests.post(
            f"https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,authors,publicationVenue,year,citations,citations.title,citations.authors",
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
            is_journal = venue == "journal"
            analysed.append(
                CitationAnalysis(paper=paper, own=own_citations, nonown=nonown_citations,
                                 year=data["year"],
                                 journal=is_journal))
        return analysed


class ScopusResolver:
    def name(self) -> str:
        return "Scopus"

    def url(self) -> str:
        return "https://www.scopus.com"

    def resolve(self, papers: List[Paper]) -> List[CitationAnalysis]:
        from pybliometrics.scopus import AbstractRetrieval, ScopusSearch

        results = []
        for paper in tqdm.tqdm(papers, desc="Scopus loading"):
            if paper.doi is None:
                continue
            try:
                abstract = AbstractRetrieval(paper.doi.replace("\\", ""), id_type="doi")
            except pybliometrics.scopus.exception.Scopus404Error:
                print(f"{paper.bibname} not found on Scopus")
                continue
            year = int(abstract.coverDate.split("-")[0])
            paper_author_ids = set(author.auid for author in abstract.authors)
            # Refresh if too old
            citations = ScopusSearch(f"REF({abstract.eid})", refresh=1)
            own_citations = []
            nonown_citations = []
            citations = citations.results or []
            for citation in citations:
                citation_author_ids = set(int(author_id) for author_id in citation.author_ids.split(";"))
                nonown = paper_author_ids.isdisjoint(citation_author_ids)
                if nonown:
                    nonown_citations.append(citation.title)
                else:
                    own_citations.append(citation.title)
            is_journal = abstract.aggregationType.lower() == "journal"
            results.append(CitationAnalysis(paper=paper, own=own_citations, nonown=nonown_citations,
                                            year=year,
                                            journal=is_journal))
        return results


def calculate_h_index(results: List[CitationAnalysis], include_own_citations=False) -> int:
    citation_counts = []
    for result in results:
        citation_count = len(result.nonown)
        if include_own_citations:
            citation_count += len(result.own)
        citation_counts.append(citation_count)
    for index in range(max(citation_counts), -1, -1):
        count = sum(1 if c >= index else 0 for c in citation_counts)
        if count >= index:
            return index
    assert False


if __name__ == "__main__":
    papers: List[Paper] = [
        Paper(bibname="hyperqueue", doi="10.1016/j.softx.2024.101814", related=True, index="SCOPUS",
              SJR=0.544),
        Paper(bibname="rsds", doi="10.1109/WORKS51914.2020.00006", related=True, index="SCOPUS"),
        Paper(bibname="estee", doi="10.1007/s11227-022-04438-y", related=True, index="SCOPUS",
              SJR=0.684),
        Paper(bibname="ligate", doi="10.1145/3587135.3592172", related=True, index="SCOPUS"),
        Paper(bibname="sisa", doi="10.1145/3466752.3480133", index="SCOPUS"),
        Paper(bibname="graphminesuite", doi="10.14778/3476249.3476252", index="SCOPUS", SJR=2.376),
        Paper(bibname="spin", doi="10.1145/3295500.3356189", index="SCOPUS"),
        Paper(bibname="spin2", doi="10.1109/ISCA52012.2021.00079", index="SCOPUS"),
        Paper(bibname="pspin", arxiv="2010.03536"),
        Paper(bibname="smi", doi="10.1145/3295500.3356201", index="SCOPUS"),
        Paper(bibname="haydi", doi="10.1007/978-3-319-90050-6\\_8", index="SCOPUS"),
        Paper(bibname="pycaverdock", doi="10.1093/bioinformatics/btad443", index="SCOPUS",
              impact_factor=5.8),
        Paper(bibname="traffic_simulator_1", doi="10.1007/978-3-030-29029-0_22", index="SCOPUS"),
        Paper(bibname="traffic_simulator_2", doi="10.1007/978-3-030-22354-0_27", index="SCOPUS"),
    ]

    # resolver = SemanticScholarResolver()
    resolver = ScopusResolver()
    analysed = resolver.resolve(papers)
    aggregated = {res.paper.bibname: res for res in analysed}

    h_index = calculate_h_index(analysed)
    total_nonown_citations = sum(len(analysis.nonown) for analysis in analysed)
    total_own_citations = sum(len(analysis.own) for analysis in analysed)
    print(f"Own citations: {total_own_citations}, non-own citations: {total_nonown_citations}, h-index: {h_index}")

    related = [analysis for analysis in analysed if analysis.paper.related]
    nonrelated = [analysis for analysis in analysed if not analysis.paper.related]

    # Inspiration taken from https://tex.stackexchange.com/a/304968/95679
    now = datetime.datetime.now()
    date_formatted = now.strftime("%-d. %-m. %Y")
    with open("chapters/publications-generated.tex", "w") as f:
        f.write(
            f"""All citation data presented below is actual as of {date_formatted}, unless otherwise
            specified. Citation data was taken from {resolver.name()}\\footnoteurl{{{resolver.url()}}}.
Self-citation is defined as a citation with a non-empty intersection between the authors of the citing and the cited paper.
SJR (Scientific Journal Rankings) ranking was taken from Scimago Journal\\footnoteurl{{https://www.scimagojr.com}},
IF (Impact Factor) ranking was taken from Oxford Academic\\footnoteurl{{https://academic.oup.com/bioinformatics}}.
The h-index of the author of this thesis according to the Scopus database is \\texttt{{{h_index}}},
with \\texttt{{{total_nonown_citations}}} total citations (both excluding self-citations).

Note that Ada Böhm was named Stanislav Böhm in older publications.
""")

        f.write(r"""
\begin{refsection}
\renewcommand*{\mkbibnamegiven}[1]{%
	\ifitemannotation{highlight}
	{\textbf{#1}}
	{#1}}

\renewcommand*{\mkbibnamefamily}[1]{%
	\ifitemannotation{highlight}
	{\textbf{#1}}
	{#1}}

\section*{Publications Related to Thesis}
""")

        f.write("\t\\begin{itemize}\n")
        for item in related:
            f.write(format_entry(item))
        f.write("\t\\end{itemize}\n")

        f.write("""
\\section*{Publications Not Related to Thesis}
\t\\begin{itemize}
""")
        for item in nonrelated:
            f.write(format_entry(item))
        f.write("\t\\end{itemize}\n")
        f.write("\\end{refsection}\n")
