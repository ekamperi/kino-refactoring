import subprocess
import json


def test_against_ground_truth():
    """
    The tests/ground_truth1.json is a relatively small file,
    compared to tests/ground_truth{2,3}.json files.
    """
    for idx in range(1, 4):
        with open(f"tests/ground_truth{idx}.json") as json_file:
            io_dict = json.load(json_file)
            for cmd in io_dict.keys():
                result = subprocess.check_output(cmd, shell=True, text=True)
                assert result == io_dict[cmd]
