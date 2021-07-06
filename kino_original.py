import argparse
import itertools as it
import json
import sys
from collections import namedtuple
from datetime import datetime

import requests

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

Draw = namedtuple("Draw", ["id", "numbers"])

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="KINO payout calculator",
)
parser.add_argument(
    "numbers",
    nargs="+",
    type=int,
    choices=range(1, 81),
    metavar="NUMBER",
    help="One or more selected numbers, up to 12",
)
parser.add_argument(
    "-d",
    "--date",
    default=str(datetime.today().date()),
    help="Draw date in YYYY-MM-DD format",
)
parser.add_argument(
    "-p",
    "--page",
    type=int,
    choices=range(1, 19),
    nargs="+",
    metavar="PAGE",
    help="Fetch only the given page(s) of draws for the given date",
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="Log each draw for debugging",
)

opts = parser.parse_args()
n = len(opts.numbers)
if n > 12:
    parser.error("Up to 12 numbers can be selected")
if n != len(set(opts.numbers)):
    parser.error("Selected numbers can not contain duplicates")

try:
    opts.date = datetime.strptime(opts.date, "%Y-%m-%d").date()
except ValueError as ex:
    parser.error(ex)

draws = []
pages = opts.page or []
session = requests.Session()
url = f"https://api.opap.gr/draws/v3.0/1100/draw-date/{opts.date}/{opts.date}"
if pages:
    for page in pages:
        resp = session.get(url, params={"page": page - 1}).json()
        for draw in resp["content"]:
            draws.append(Draw(draw["drawId"], draw["winningNumbers"]["list"]))
else:  # fetch all pages
    for page in it.count(start=1):
        resp = session.get(url, params={"page": page - 1}).json()
        if resp["content"]:
            pages.append(page)
            for draw in resp["content"]:
                draws.append(Draw(draw["drawId"], draw["winningNumbers"]["list"]))
        if resp["last"]:
            break

selected = frozenset(opts.numbers)
selected_payouts = PAYOUT_TABLE[len(selected)]
payouts = []
for draw in draws:
    matches = selected.intersection(draw.numbers)
    payout = selected_payouts.get(len(matches), 0)
    payouts.append(payout)
    if opts.debug:
        print(f"{draw}: matches={sorted(matches)}, payout={payout}", file=sys.stderr)

result = {
    "selected_numbers": opts.numbers,
    "date": str(opts.date),
    "pages": pages,
    "num_payouts": len(payouts),
    "mean_payout": sum(payouts) / len(payouts) if payouts else None,
}
print(json.dumps(result))
