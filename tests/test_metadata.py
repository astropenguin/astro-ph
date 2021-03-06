# third-party packages
import astro_ph
from typing_extensions import Final


# constants
AUTHOR: Final[str] = "Akio Taniguchi"
VERSION: Final[str] = "0.2.4"


# test functions
def test_author() -> None:
    assert astro_ph.__author__ == AUTHOR


def test_version() -> None:
    assert astro_ph.__version__ == VERSION
