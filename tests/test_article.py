# third-party packages
from astro_ph.article import detex
from pytest import mark
from typing_extensions import Final


# constants
testdata: Final[tuple] = (
    ("This is \\textbf{a bold text}.", "This is a bold text."),
    ("This is {\\textbf a bold text}.", "This is a bold text."),
    ("This is \\emph{emphasized}.", "This is emphasized."),
    ("This is {\\em emphasized}.", "This is emphasized."),
    ("This has   \n irregular\nbreaks.", "This has irregular breaks."),
)


# test functions
@mark.parametrize("original, detexed", testdata)
def test_detex(original: str, detexed: str) -> None:
    assert detex(original) == detexed
