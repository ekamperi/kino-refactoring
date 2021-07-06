#!/usr/bin/env python3

"""
This is a utility to generate ground truth data to use in tests. We generate,
execute, and store the results of random unix shell command line invocations
of the original kino implementation. Then, while testing, we execute the same
exact invocation but we replace the original kino implementation with our own.
The output of this script is a JSON formatted string of a dictionary, where
the keys are the commands and the values are the expected outputs.
"""

from random import sample, randint
import datetime
import json
import subprocess


def date_range(start_date, end_date):
    """A generator that yields a sequence of dates starting from
    `start_date' up to `end_date' (not inclusive).
    """
    days_between = int((end_date - start_date).days)
    for n in range(days_between):
        yield start_date + datetime.timedelta(n)


def get_random_selected_numbers():
    """Returns a list of random integer numbers in the range [1, 80].
    The list itself has a random length in the range [1,12].
    """
    return sample(range(1, 81), randint(1, 12))


def get_random_pages():
    """Returns a list of random integer numbers in the range [1, 18].
    The list itself has a random length in the range [1, 18].
    """
    return sample(range(1, 19), randint(1, 18))


def list2str(lst):
    """Converts a list of integers into a list of strings and
    concatenates them by using a single space as a delimeter.
    The resultant string is returned.

    E.g., the list [1, 2, 3] becomes the string "1 2 3".
    """
    return " ".join([str(x) for x in lst])


def date2str(date):
    """Returns `date' as a formatted string of the form year-month-day."""
    return date.strftime("%Y-%m-%d")


def gen_cmd(numbers, pages, date):
    """Returns a unix shell command given a list of numbers, pages, and dates.
    The inclusion of pages is decided stochastically, so that we create a more
    diverse testing set.

    E.g., given numbers = [1, 2, 3], pages = [1, 2] and date = 2020-5-15 it will generate
    the following command:
        python3 kino_original.py 1 2 3 -p 1 2 -d 2020-5-15

    kino_original.py is the unmodified, original file before the refactoring.
    """
    ln = list2str(numbers)
    cmd = f"python3 kino_original.py {ln}"

    # Decide by chance whether we will specify --pages
    if randint(0, 2):
        lp = list2str(pages)
        cmd = cmd + f" -p {lp}"

    ds = date2str(date)
    cmd = cmd + f" -d {ds}"
    return cmd


def main():
    # This is the date range of the ground truth data that we will generate.
    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date(2021, 4, 1)

    # This is the dictionary where we will save our ground truth data.
    # The key will be the unix shell command and the value will be the
    # output of the unix shell command invocation.
    io_dict = {}

    # Iterate over the specified date range
    for some_date in date_range(start_date, end_date):
        # Generate random selected numbers, and pages.
        numbers = get_random_selected_numbers()
        pages = get_random_pages()

        # Generate the unix shell command for this particular date.
        cmd = gen_cmd(numbers, pages, some_date)

        # Execute the unix shell command and save the result into
        # the dictionary. FIXME: We may need to limit the rate at
        # which we are submitting http requests to opap's REST API.
        # Currently, we don't.
        result = subprocess.check_output(cmd, shell=True, text=True)

        # Before saving the result to the dictionary, replace the
        # "kino_original.py" with "kino.py" in the `cmd', so that
        # when we execute the tests, our refactored implementation
        # will get called. Otherwise, we will checking against a tautology.
        cmd = cmd.replace("kino_original.py", "kino.py")
        io_dict[cmd] = result

    # Serialize the dictionary as JSON formatted string and print it.
    print(json.dumps(io_dict))


if __name__ == "__main__":
    main()
