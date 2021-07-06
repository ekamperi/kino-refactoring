import itertools as it
from collections import namedtuple
import requests
from url_builder import UrlBuilder


class KinoFetch:
    def __init__(self, memory=None):
        self.session = requests.Session()
        # We cannot decorate a method at class definition, because
        # when the class is instantiated, the first argument (self)
        # is bound, and no longer accessible to joblib's Memory object.
        # Instead, manually decorate, at instantiation time, the class
        # method for which we want to enable caching.
        if memory:
            self._fetch_draws_for_page = memory.cache(self._fetch_draws_for_page)

    def _fetch_draws_for_page(self, page, from_date, to_date):
        """Returns a tuple where the first element is a boolean on whether we
        hit the last element, and the second element is a list of draws for this
        particular `page'.
        """
        Draw = namedtuple("Draw", ["id", "numbers"])
        url = UrlBuilder().get_in_date_range(from_date, to_date)
        resp = self.session.get(url, params={"page": page - 1}).json()
        draws = []
        if resp["content"]:
            for draw in resp["content"]:
                draws.append(Draw(draw["drawId"], draw["winningNumbers"]["list"]))
        return resp["last"], draws

    def fetch_winning_nums(self, pages, from_date, to_date):
        """Returns pages and draws for the current date range. If `pages' is empty,
        then we will request data for all pages.
        """
        draws = []
        if pages:
            for page in pages:
                _, new_draws = self._fetch_draws_for_page(page, from_date, to_date)
                draws = draws + new_draws
        else:  # fetch all pages
            for page in it.count(start=1):
                is_last, new_draws = self._fetch_draws_for_page(
                    page, from_date, to_date
                )
                draws = draws + new_draws
                pages.append(page)
                if is_last:
                    break
        return pages, draws
