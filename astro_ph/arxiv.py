__all__ = ["Article", "Search"]


# standard library
from datetime import date, datetime, time, timedelta
from dataclasses import dataclass, field, replace
from typing import Sequence, Union


# third-party packages
import arxiv
from typing_extensions import Final
from .deepl import Driver, Language, translate


# constants
ABS: Final[str] = "abs"
AND: Final[str] = "AND"
ARXIV_URL: Final[str] = "arxiv_url"
AUTHORS: Final[str] = "authors"
CAT: Final[str] = "cat"
DATE: Final[str] = "submittedDate"
DATE_FORMAT: Final[str] = "%Y%m%d%H%M%S"
OR: Final[str] = "OR"
SEPARATOR: Final[str] = "++++++++++"
SUMMARY: Final[str] = "summary"
TITLE: Final[str] = "title"
TO: Final[str] = "TO"


# main features
@dataclass
class Article:
    """Article class to store an article information."""

    title: str  #: Title of an article.
    authors: Sequence[str]  #: Author(s) of an article.
    summary: str  #: Summary of an article.
    arxiv_url: str  #: arXiv URL of an article.

    def __post_init__(self) -> None:
        self.title = self.title.replace("\n", " ")
        self.summary = self.summary.replace("\n", " ")

    @classmethod
    def from_arxiv_result(cls, result: dict) -> "Article":
        """Return an article from a result of arXiv query."""
        return cls(
            title=result[TITLE],
            authors=result[AUTHORS],
            summary=result[SUMMARY],
            arxiv_url=result[ARXIV_URL],
        )

    def translate(
        self,
        lang_to: Language = Language.AUTO,
        lang_from: Language = Language.AUTO,
        driver: Driver = Driver.CHROME,
    ) -> "Article":
        """Return an article whose title and summary are translated."""
        text = f"{self.title}\n{SEPARATOR}\n{self.summary}"
        text_new = translate(text, lang_to, lang_from, driver)
        title_new, summary_new = text_new.split(SEPARATOR)

        return replace(self, title=title_new, summary=summary_new)


@dataclass
class Search:
    """Search class to search for articles in arXiv."""

    date_start: Union[datetime, str]  #: Start date for a search (inclusive).
    date_end: Union[datetime, str]  #: End date for a search (exclusive).
    keywords: Sequence[str] = field(default_factory=list)  #: Keywords for a search.
    categories: Sequence[str] = field(default_factory=list)  #: arXiv categories.

    def __post_init__(self) -> None:
        if not isinstance(self.date_start, datetime):
            self.date_start = datetime.fromisoformat(self.date_start)

        if not isinstance(self.date_end, datetime):
            self.date_end = datetime.fromisoformat(self.date_end)

    def run(self) -> Sequence[Article]:
        """Run a search and return articles found in arXiv."""
        results = arxiv.query(self.to_arxiv_query())
        return [Article.from_arxiv_result(result) for result in results]

    def to_arxiv_query(self) -> str:
        """Convert an instance to a query for the arXiv API."""
        date_start = self.date_start.strftime(DATE_FORMAT)
        date_end = (self.date_end - timedelta(seconds=1)).strftime(DATE_FORMAT)

        query = f"{DATE}:[{date_start} {TO} {date_end}]"

        if self.categories:
            subquery = f" {OR} ".join(f"{CAT}:{cat}" for cat in self.categories)
            query += f" {AND} ({subquery})"

        if self.keywords:
            subquery = f" {OR} ".join(f"{ABS}:{kwd}" for kwd in self.keywords)
            query += f" {AND} ({subquery})"

        return query


# helper features
def get_today() -> datetime:
    """Return a datetime instance to indicate today."""
    return datetime.combine(date.today(), time())
