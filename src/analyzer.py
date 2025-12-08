from collections import Counter, namedtuple
import re

Result = namedtuple("Result", ["total_tickets", "frequencies", "top_numbers"])

_NUMBER_RE = re.compile(r"-?\d+")

def analyze(path, top_n=10):
    """
    Read the file at `path`, parse numeric tokens on each non-empty line,
    count frequencies across all numbers, and return a Result:
      - total_tickets: number of non-empty lines parsed
      - frequencies: list of (number, count) sorted ascending by number
      - top_numbers: list of (number, count) sorted by count desc
    Non-numeric tokens are ignored.
    """
    counter = Counter()
    total_lines = 0

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            total_lines += 1
            # find integers in the line
            nums = _NUMBER_RE.findall(line)
            for n in nums:
                try:
                    num = int(n)
                    counter[num] += 1
                except ValueError:
                    continue

    freqs_sorted = sorted(counter.items(), key=lambda x: x[0])  # by number
    top = counter.most_common(top_n)

    return Result(total_tickets=total_lines, frequencies=freqs_sorted, top_numbers=top)
