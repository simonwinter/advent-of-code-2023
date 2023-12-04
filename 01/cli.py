import re
from collections import deque

import click

nums = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part1Match(line):
    matches = re.findall("\d", line)

    if matches:
        return int(matches[0] + matches[-1])

    return 0


def part2Match(line):
    matches = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

    if matches:
        first = matches[0] if matches[0] not in nums else nums[matches[0]]
        last = matches[-1] if matches[-1] not in nums else nums[matches[-1]]

        return int(first + last)

    return 0


def findMatch(line, part):
    if part == "1":
        return part1Match(line)

    return part2Match(line)


@click.command()
@click.option(
    "--part",
    type=click.Choice(["1", "2"]),
    default="1",
)
@click.argument("file", type=click.File(mode="r"))
def cli(file, part):
    matches = [findMatch(line, part) for line in deque(file)]
    click.echo(matches, nl=True)
    click.echo(sum(matches), nl=True)


if __name__ == "__main__":
    cli()
