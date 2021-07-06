from time import perf_counter
from tempfile import gettempdir
from joblib import Memory

from kino_fetch import KinoFetch


def test_caching():
    memory = Memory(gettempdir(), verbose=0)
    kf_caching = KinoFetch(memory=memory)
    kf_no_caching = KinoFetch(memory=None)

    n_rep = 10

    # No caching
    start = perf_counter()
    for _ in range(n_rep):
        pages = []
        pages, draws_no_caching = kf_no_caching.fetch_winning_nums(
            pages, "2021-05-15", "2021-05-15"
        )
    time_no_caching = (perf_counter() - start) / n_rep
    assert pages

    # With caching -- first fetch via network, and then from local disk.
    start = perf_counter()
    pages = []
    pages, draws_caching = kf_caching.fetch_winning_nums(
        pages, "2021-05-15", "2021-05-15"
    )
    time_warmup = perf_counter() - start
    assert pages

    start = perf_counter()
    for _ in range(n_rep):
        pages = []
        pages, draws_caching = kf_caching.fetch_winning_nums(
            pages, "2021-05-15", "2021-05-15"
        )
    time_caching = (perf_counter() - start) / n_rep
    assert pages

    # Make sure we are getting the same results
    assert draws_no_caching == draws_caching

    # print(time_no_caching, time_warmup, time_caching)
    # doesn't show any significant speedup. However by setting verbose=1
    # when instantiating Memory(), and running the tests with -s flag,
    # we confirm that we are serving cached data. Apparently, the cost
    # of fetching over the network is comparable to fetching from local disk.

