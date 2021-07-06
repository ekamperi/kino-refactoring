from collections import namedtuple

from payouts import Payouts, PAYOUT_TABLE


def test_payouts():
    # Let the winning numbers be equal to [1, 2, 3, 4, 5, 6, ..., 20].
    # Then, we progressively set the selected numbers to be
    # [1], then [1, 2], then [1, 2, 3], ..., [1, 2, 3, ..., 12]
    # It could probably be done with fixture parameterization, but
    # I found it more straightforward this way.
    Draw = namedtuple("Draw", ["id", "numbers"])
    draws = [Draw(id=1, numbers=[x for x in range(1, 21)])]

    for i in range(1, 13):
        selected_numbers = [x for x in range(1, i + 1)]
        p = Payouts(selected_numbers, draws)
        assert p.get_num_payouts() == 1
        assert p.get_mean_payout() == PAYOUT_TABLE[i][i]


def test_payouts2():
    # Let the winning numbers be [1, 2, 3, ..., 20] and [2, 3, 4, ..., 20]
    # in the 1st and in the 2nd draw, respectively.
    # As previously, we progressively consider the selected numbers to be
    # [1], then [1, 2], then [1, 2, 3], ..., [1, 2, 3, ..., 12]
    Draw = namedtuple("Draw", ["id", "numbers"])
    draws = [
        Draw(id=1, numbers=[x for x in range(1, 21)]),
        Draw(id=2, numbers=[x for x in range(2, 22)]),
    ]

    for i in range(2, 13):
        selected_numbers = [x for x in range(1, i + 1)]
        p = Payouts(selected_numbers, draws)
        assert p.get_num_payouts() == 2
        expected_mean_payout = (PAYOUT_TABLE[i][i] + PAYOUT_TABLE[i][i - 1]) / 2.0
        assert p.get_mean_payout() == expected_mean_payout
