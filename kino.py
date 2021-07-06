from joblib import Memory

from fetch import KinoFetch
from parser import KinoParser
from payouts import Payouts
from results import Results


opts = KinoParser().parse_and_validate_args()
pages = opts.page or []

memory = Memory(opts.cache, verbose=0) if opts.cache else None

pages, draws = KinoFetch(memory).fetch_winning_nums(pages, opts.date, opts.date)
payouts = Payouts(opts.numbers, draws)
result = Results.get_results(opts, pages, payouts)
print(result)
