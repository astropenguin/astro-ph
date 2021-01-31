__all__ = ["DeepL", "Language", "translate"]


# standard library
import asyncio
from dataclasses import dataclass
from enum import auto, Enum
from typing import Awaitable, Union
from urllib.parse import quote


# third-party packages
from pyppeteer import launch
from typing_extensions import Final


# constants
URL: Final[str] = "https://www.deepl.com/translator"
JS_FUNC: Final[str] = "element => element.textContent"
SELECTOR: Final[str] = ".lmt__translations_as_text__text_btn"
TIMEOUT: Final[int] = 30


# main features
class Language(Enum):
    """Available languages for translation."""

    AUTO = auto()  #: Auto language detection
    DE = auto()  #: German
    EN = auto()  #: English
    FR = auto()  #: French
    IT = auto()  #: Italian
    JA = auto()  #: Japanese
    ES = auto()  #: Spanish
    NL = auto()  #: Dutch
    PL = auto()  #: Polish
    PT = auto()  #: Portuguese
    RU = auto()  #: Russian
    ZH = auto()  #: Chinese


@dataclass
class DeepL:
    lang_from: Union[Language, str] = Language.AUTO  #: Language of original text.
    lang_to: Union[Language, str] = Language.AUTO  #: Language of translated text.
    timeout: int = TIMEOUT  #: Timeout for translation (in seconds).

    def __post_init__(self) -> None:
        if isinstance(self.lang_from, str):
            self.lang_from = Language[self.lang_from.upper()]

        if isinstance(self.lang_to, str):
            self.lang_to = Language[self.lang_to.upper()]

        self.url = f"{URL}#/{self.lang_from.name}/{self.lang_to.name}"

    async def translate(self, text: str) -> Awaitable[str]:
        """Translate text written in one language to another."""
        browser = await launch()
        page = await browser.newPage()
        page.setDefaultNavigationTimeout(self.timeout * 1000)
        completion = self.translation_completion(page)

        try:
            await page.goto(f"{self.url}/{quote(text)}")
            return await asyncio.wait_for(completion, self.timeout)
        except asyncio.TimeoutError as err:
            raise type(err)("Translation was timed out.")
        finally:
            await browser.close()

    async def translation_completion(self, page) -> Awaitable[str]:
        """Wait for completion of translation and return result."""
        translated = ""

        while not translated:
            await asyncio.sleep(1)
            element = await page.querySelector(SELECTOR)
            translated = await page.evaluate(JS_FUNC, element)

        return translated


def translate(
    text: str,
    lang_to: Union[Language, str] = Language.AUTO,
    lang_from: Union[Language, str] = Language.AUTO,
    timeout: int = TIMEOUT,
) -> str:
    """Translate text written in one language to another.

    Args:
        text: Text to be translated.
        lang_to: Language to which the text is translated.
        lang_from: Language of the original text.
        timeout: Timeout for translation (in seconds).

    Returns:
        Translated text.

    """
    deepl = DeepL(lang_from, lang_to, timeout)
    return asyncio.run(deepl.translate(text))
