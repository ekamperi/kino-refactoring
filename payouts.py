import sys

PAYOUT_TABLE = [
    {},
    {1: 2.5},
    {2: 5, 1: 1},
    {3: 25, 2: 2.5},
    {4: 100, 3: 4, 2: 1},
    {5: 450, 4: 20, 3: 2},
    {6: 1_600, 5: 50, 4: 7, 3: 1},
    {7: 5_000, 6: 100, 5: 20, 4: 3, 3: 1},
    {8: 15_000, 7: 1_000, 6: 50, 5: 10, 4: 2},
    {9: 40_000, 8: 4_000, 7: 200, 6: 25, 5: 5, 4: 1},
    {10: 100_000, 9: 10_000, 8: 500, 7: 80, 6: 20, 5: 2, 0: 2},
    {11: 500_000, 10: 15_000, 9: 1_500, 8: 250, 7: 50, 6: 10, 5: 1, 0: 2},
    {12: 1_000_000, 11: 25_000, 10: 2_500, 9: 1_000, 8: 150, 7: 25, 6: 5, 0: 4},
]


class Payouts:
    def __init__(self, selected_numbers, draws, debug=False):
        self.selected_numbers = selected_numbers
        self.draws = draws
        self.debug = debug
        self.payouts = []
        self._calc_payouts()

    def _calc_payouts(self):
        """Calculates the payouts given a set of selected numbers and the draws."""
        selected = frozenset(self.selected_numbers)
        selected_payouts = PAYOUT_TABLE[len(selected)]
        self.payouts = []
        for draw in self.draws:
            matches = selected.intersection(draw.numbers)
            payout = selected_payouts.get(len(matches), 0)
            self.payouts.append(payout)
            if self.debug:
                print(
                    f"{draw}: matches={sorted(matches)}, payout={payout}",
                    file=sys.stderr,
                )
        return self.payouts

    def get_payouts(self):
        """Returns the list of payouts."""
        return self.payouts

    def get_num_payouts(self):
        """Returns the number of payouts."""
        return len(self.payouts)

    def get_mean_payout(self):
        """Returns the mean payout."""
        return sum(self.payouts) / len(self.payouts) if self.payouts else None
