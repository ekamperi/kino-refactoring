import pytest

from url_builder import UrlBuilder


@pytest.fixture(name="url_builder")
def fixture_url_builder():
    return UrlBuilder()


def test_get_in_date_range(url_builder):
    url = url_builder.get_in_date_range(from_date="2021-05-14", to_date="2021-05-14")
    assert url == "https://api.opap.gr/draws/v3.0/1100/draw-date/2021-05-14/2021-05-14"


def test_get_last_result_and_active(url_builder):
    url = url_builder.get_last_result_and_active()
    assert url == "https://api.opap.gr/draws/v3.0/1100/last-result-and-active"


def test_get_statistics(url_builder):
    with pytest.raises(ValueError):
        url_builder.get_statistics(draw_range=0)

    # Only 12 and 1801 are valid `draw_range' values
    for draw_range in [12, 1801]:
        url = url_builder.get_statistics(draw_range)
        assert (
            url
            == f"https://api.opap.gr/games/v1.0/1100/statistics?drawRange={draw_range}"
        )
