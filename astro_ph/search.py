from __future__ import annotations


# standard library
import asyncio
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import AsyncIterable, Awaitable, Iterable, Optional, Sequence, Union


# third-party packages
from aiohttp import ClientSession, TCPConnector
from feedparser import FeedParserDict, parse
from typing_extensions import Final
from .detex import detex


# constants
ARXIV_API: Final[str] = "http://export.arxiv.org/api/query"
DATE_FORMAT: Final[str] = "%Y%m%d%H%M%S"
SECOND: Final[timedelta] = timedelta(seconds=1)
SEPARATOR: Final[str] = "++++++++++"


# data classes
@dataclass
class Article:
    """Article class for storing article information."""

    title: str  #: Title of an article.
    authors: Sequence[str]  #: Author(s) of an article.
    summary: str  #: Summary of an article.
    arxiv_url: str  #: arXiv URL of an article.

    def __post_init__(self) -> None:
        self.title = detex(self.title)
        self.summary = detex(self.summary)

    def replace(self, text: str, translated: str) -> Article:
        """Method necessary to become translatable."""
        title, summary = translated.split(SEPARATOR)
        return replace(self, title=title, summary=summary)

    def __str__(self) -> str:
        """Method necessary to become translatable."""
        return f"{self.title}\n{SEPARATOR}\n{self.summary}"


@dataclass
class Search:
    """Search class for searching for articles in arXiv."""

    date_start: Union[datetime, str]  #: Start date for a search (inclusive).
    date_end: Union[datetime, str]  #: End date for a search (exclusive).
    keywords: Optional[Sequence[str]] = None  #: Keywords for a search.
    categories: Optional[Sequence[str]] = None  #: arXiv categories.
    n_max_articles: int = 1000  #: Maximum number of articles to get.
    n_per_request: int = 100  #: Number of articles to get per request.
    n_parallel: int = 1  #: Number of simultaneous requests (do not change).

    def __post_init__(self) -> None:
        if not isinstance(self.date_start, datetime):
            self.date_start = datetime.fromisoformat(self.date_start)

        if not isinstance(self.date_end, datetime):
            self.date_end = datetime.fromisoformat(self.date_end)

    @property
    def search_query(self) -> str:
        """Convert to search query for the arXiv API."""
        date_start = self.date_start.strftime(DATE_FORMAT)
        date_end = (self.date_end - SECOND).strftime(DATE_FORMAT)

        query = f"submittedDate:[{date_start} TO {date_end}]"

        if self.categories:
            sub = " OR ".join(f"cat:{cat}" for cat in self.categories)
            query += f" AND ({sub})"

        if self.keywords:
            sub = " OR ".join(f"abs:{kwd}" for kwd in self.keywords)
            query += f" AND ({sub})"

        return query

    def __aiter__(self) -> AsyncIterable[Article]:
        """Search for articles and yield them as article instances."""

        async def search():
            async for entry in self._search():
                yield entry.title.replace("\n", " ")

        return search()

    async def _search(self) -> AsyncIterable[FeedParserDict]:
        """Search for articles and yield them as Atom entries."""
        connector = TCPConnector(limit=self.n_parallel)

        async with ClientSession(connector=connector) as client:
            requests = list(self._gen_requests(client))

            for request in asyncio.as_completed(requests):
                feed = parse(await request)

                for entry in feed.entries:
                    yield entry

    def _gen_requests(self, client: TCPConnector) -> Iterable[Awaitable]:
        """Generate coroutines to request the arXiv results."""

        async def request(url: str, **params) -> Awaitable[str]:
            async with client.get(url, params=params) as resp:
                return await resp.text()

        for start in range(0, self.n_max_articles, self.n_per_request):
            yield request(
                ARXIV_API,
                search_query=self.search_query,
                start=start,
                max_results=self.n_per_request,
            )
