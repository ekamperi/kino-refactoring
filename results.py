import json


class Results:
    @staticmethod
    def get_results(opts, pages, payouts):
        """Returns a JSON formatted string with selected numbers,
        date, pages, number of payouts and mean payout.
        """
        result = {
            "selected_numbers": opts.numbers,
            "date": str(opts.date),
            "pages": pages,
            "num_payouts": payouts.get_num_payouts(),
            "mean_payout": payouts.get_mean_payout(),
        }
        return json.dumps(result)
