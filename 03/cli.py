import re
from collections import deque

import click


def findPaddedLine(fileIO, key, val_len, i, num_lines):
    """
    Take the current line, pad by 1 character before & after. Do the same for the
    previous & next lines (if available).

    e.g. a line matching "711" becomes:

    .....\n
    .711.\n
    .....\n

    (where . represents characters on previous/next lines).
    """
    line_len = len(fileIO[i])
    start = key - 1 if key != 0 else key
    end = key + val_len + 1 if (key + val_len) < line_len - 2 else line_len - 2

    current = fileIO[i][start:end]
    previous = fileIO[i - 1][start:end] if i > 0 else ""
    next = fileIO[i + 1][start:end] if i < num_lines - 1 else ""

    return (current, previous, next)


def filterPaddedMatch(paddedLines):
    """
    check to see if padded lines contain adjacent symbols (non digits or periods).
    """
    (current, previous, next) = paddedLines

    found = False
    for ends in [previous, current, next]:
        _match = re.search("[^\.\d]", ends)
        if _match:
            found = True

    return found


@click.command()
@click.argument("file", type=click.File(mode="r"))
def cli(file):
    fileIO = deque(file)
    lines = [
        {
            m.start(0): (int(m.group(0)), len(m.group(0)))
            for m in re.finditer("\d+", line)
        }
        for line in fileIO
    ]

    part_numbers = []
    for i, line in enumerate(lines):
        parts = [
            val
            for key, (val, val_len) in line.items()
            if filterPaddedMatch(findPaddedLine(fileIO, key, val_len, i, len(lines)))
        ]

        part_numbers = part_numbers + parts

    click.echo(sum(part_numbers))


if __name__ == "__main__":
    cli()
