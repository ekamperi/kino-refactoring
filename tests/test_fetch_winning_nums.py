from collections import namedtuple
import pytest

from kino_fetch import KinoFetch


@pytest.fixture(name="kf")
def fixture_kf():
    return KinoFetch(memory=None)


def test_fetch_winning_nums_empty_pages(kf):
    pages = []
    pages, _ = kf.fetch_winning_nums(pages, "2021-05-15", "2021-05-15")
    assert pages  # Make sure pages is populated


def test_fetch_winning_nums_page_1_draw_0(kf):
    """
    This is a hard-coded very specific test, as a quick
    check whether some basic functionality works or not.
    """
    Draw = namedtuple("Draw", ["id", "numbers"])

    # This is kinda ugly, but it's black's fault.
    expected_draw = Draw(
        id=878229,
        numbers=[
            38,
            59,
            75,
            2,
            61,
            29,
            41,
            5,
            23,
            57,
            48,
            21,
            77,
            19,
            58,
            56,
            8,
            64,
            55,
            9,
        ],
    )

    pages = [1]
    pages, draws = kf.fetch_winning_nums(pages, "2021-05-15", "2021-05-15")
    assert pages == [1]  # Make sure pages isn't modified
    assert draws[0] == expected_draw
