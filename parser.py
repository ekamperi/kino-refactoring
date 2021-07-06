import argparse
from datetime import datetime


class KinoParser:
    def __init__(self):
        """Creates the argument parser and define how a single
        command-line argument should be parsed.
        """
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="KINO payout calculator",
        )
        self.parser.add_argument(
            "numbers",
            nargs="+",
            type=int,
            choices=range(1, 81),
            metavar="NUMBER",
            help="One or more selected numbers, up to 12",
        )
        self.parser.add_argument(
            "-d",
            "--date",
            default=str(datetime.today().date()),
            help="Draw date in YYYY-MM-DD format",
        )
        self.parser.add_argument(
            "-p",
            "--page",
            type=int,
            choices=range(1, 19),
            nargs="+",
            metavar="PAGE",
            help="Fetch only the given page(s) of draws for the given date",
        )
        self.parser.add_argument(
            "-c", "--cache", metavar="DIR", help="Directory to use for caching"
        )
        self.parser.add_argument(
            "--debug",
            action="store_true",
            help="Log each draw for debugging",
        )

    def parse_and_validate_args(self):
        """
        Parses the user-supplied arguments and validates them.
        There can't be more than 12 numbers and they must be unique.
        Also the date must be in year-month-day format. The function
        returns the populated namespace with argument strings assigned
        as attributes to the namespace.
        """
        opts = self.parser.parse_args()
        n = len(opts.numbers)
        if n > 12:
            self.parser.error("Up to 12 numbers can be selected")
        if n != len(set(opts.numbers)):
            self.parser.error("Selected numbers can not contain duplicates")

        try:
            opts.date = datetime.strptime(opts.date, "%Y-%m-%d").date()
        except ValueError as ex:
            self.parser.error(ex)

        return opts
