# standard library
import asyncio
from datetime import date, datetime, time, timedelta
from logging import basicConfig, getLevelName, getLogger
from typing import Optional, Union


# third-party packages
from fire import Fire
from typing_extensions import Final
from .apps import Slack
from .search import Search
from .translate import DeepL


# constants
COMMA: Final[str] = ","
DATE_FORMAT: Final[str] = "%Y-%m-%d"
KEYWORDS: Final[str] = "galaxy,galaxies"
CATEGORIES: Final[str] = "astro-ph.GA"
LANG_FROM: Final[str] = "en"
LANG_TO: Final[str] = "auto"
LOG_FORMAT: Final[str] = "{asctime} {name: <18} {levelname: <8} {message}"
LOG_LEVEL: Final[str] = "WARNING"
LOG_STYLE: Final[str] = "{"
N_CONCURRENT: Final[int] = 2
TIMEOUT: Final[int] = 60


# module-level logger
logger = getLogger(__name__)


# helper functions
def n_days_ago(n: int) -> str:
    """Return string of date n days ago in YYYY-mm-dd."""
    today = datetime.combine(date.today(), time())
    return (today - timedelta(days=n)).strftime(DATE_FORMAT)


def parse_multiple(obj: Union[list, tuple, str]) -> str:
    """Parse comma-separated multiple values correctly."""
    if isinstance(obj, str):
        return obj.split(COMMA)
    elif isinstance(obj, (list, tuple)):
        return COMMA.join(obj).split(COMMA)
    else:
        raise ValueError(f"Invalid value: {obj:!r}")


# subcommand functions
def slack(
    date_start: str = n_days_ago(2),
    date_end: str = n_days_ago(1),
    keywords: str = KEYWORDS,
    categories: str = CATEGORIES,
    lang_from: str = LANG_FROM,
    lang_to: str = LANG_TO,
    timeout: int = TIMEOUT,
    n_concurrent: int = N_CONCURRENT,
    webhook_url: Optional[str] = None,
    log_level: str = LOG_LEVEL,
) -> None:
    """Translate and post articles to Slack.

    Args:
        date_start: Start date for a search in YYYY-mm-dd (inclusive).
        date_end: End date for a search in YYYY-mm-dd (exclusive).
        keywords: Comma-separated keywords for a search.
        categories: Comma-separated arXiv categories.
        lang_from: Language of original text in articles.
        lang_to: Language for translated text in articles.
        timeout: Timeout for each post execution (in seconds).
        n_concurrent: Number of simultaneous execution.
        webhook_url: URL of Slack incoming webhook.
        log_level: Lowest level of log messages to show.

    Returns:
        This command does not return anything.

    """
    basicConfig(
        format=LOG_FORMAT,
        style=LOG_STYLE,
        level=getLevelName(log_level.upper()),
    )

    if webhook_url is None:
        raise ValueError("Webhook URL must be specified.")

    keywords = parse_multiple(keywords)
    categories = parse_multiple(categories)

    articles = Search(date_start, date_end, keywords, categories)
    translator = DeepL(lang_from, lang_to)
    app = Slack(translator, n_concurrent, timeout, webhook_url)

    logger.info(articles)
    logger.info(translator)
    logger.info(app)

    asyncio.run(app.post(articles))


# command line interface
def cli() -> None:
    """Entry point of command line interface."""
    Fire(dict(slack=slack))
